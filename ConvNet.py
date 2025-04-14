import torch
from einops import rearrange
from torch import nn as nn
from torch.nn import functional as F


class SWConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=(1, 1), padding=(0, 0), stride=(1, 1)):
        super().__init__()
        self.in_channels = in_channels
        self.depth_conv = nn.Conv2d(in_channels, in_channels, kernel_size=kernel_size, padding=padding,
                                    groups=in_channels, stride=stride, bias=False)
        self.point_conv = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)

    def channel_shuffle(self, x):
        groups = self.in_channels
        batch_size, num_channels, height, width = x.data.size()
        channels_per_group = num_channels // groups
        # grouping, 通道分组
        # b, num_channels, h, w =======>  b, groups, channels_per_group, h, w
        x = x.view(batch_size, groups, channels_per_group, height, width)

        # channel shuffle, 通道洗牌
        x = torch.transpose(x, 1, 2).contiguous()
        # x.shape=(batch_size, channels_per_group, groups, height, width)
        # flatten
        x = x.view(batch_size, -1, height, width)

        return x

    def forward(self, x):
        x = self.depth_conv(x)
        x = self.point_conv(x)
        # x = self.channel_shuffle(x)

        return x

class SpatialAttention(nn.Module):

    def __init__(self, kernel_size=(7, 1)):
        super(SpatialAttention, self).__init__()
        assert kernel_size in ((3, 1), (7, 1)), 'kernel size must be 3 or 7'
        padding = (3, 0) if kernel_size == (7, 1) else (1, 0)
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv1(x)
        return self.sigmoid(x)


class ConvChannelAttention(nn.Module):

    def __init__(self, in_planes, ratio=4):
        super(ConvChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc1 = nn.Conv2d(in_planes, in_planes // ratio, 1, bias=False)
        self.rReLU1 = nn.RReLU()
        self.fc2 = nn.Conv2d(in_planes // ratio, in_planes, 1, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.fc2(self.rReLU1(self.fc1(self.avg_pool(x))))
        max_out = self.fc2(self.rReLU1(self.fc1(self.max_pool(x))))
        out = avg_out + max_out
        return self.sigmoid(out)


class CBAM(nn.Module):

    def __init__(self, channel, ratio=4, kernel_size=(7, 1)):
        super(CBAM, self).__init__()
        self.channel_attention = ConvChannelAttention(channel, ratio=ratio)
        self.spatial_attention = SpatialAttention(kernel_size=kernel_size)

    def forward(self, x):
        x = x * self.channel_attention(x)
        x = x * self.spatial_attention(x)
        return x


class SELayer(nn.Module):
    def __init__(self, channel, reduction=2):
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=True),
            nn.ELU(),
            nn.Linear(channel // reduction, channel, bias=True),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


class ChannelAttention(nn.Module):
    def __init__(self, channel):
        super(ChannelAttention, self).__init__()
        self.fc1 = nn.Linear(channel, channel * 2)
        self.fc2 = nn.Linear(channel * 2, channel)
        self.softmax = nn.Softmax(-1)
        self.tanh = nn.ReLU()
        self.mean = nn.AdaptiveAvgPool2d((48, 1))


    def forward(self, x):
        x_copy = x.clone()
        x_copy = self.mean(x_copy).squeeze(-1)
        x_copy = self.fc2(self.tanh(self.fc1(x_copy)))
        x_copy = self.softmax(x_copy).unsqueeze(-1)

        return x * x_copy



class ConvNet(nn.Module):
    def __init__(self, emb_size, conv_dropout, num_classes):
        super().__init__()
        channel = 48
        self.dropout = conv_dropout
        self.scale_4_block1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=emb_size, kernel_size=(1, 4), stride=(1, 2)),
            # SELayer(emb_size, 2),
            # CBAM(emb_size, 2, ),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_4_block2 = nn.Sequential(
            nn.Conv2d(in_channels=emb_size, out_channels=emb_size, kernel_size=(48, 1), stride=(1, 1)),
            # SELayer(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_4_block3 = nn.Sequential(
            nn.Conv2d(in_channels=emb_size, out_channels=emb_size, kernel_size=(1, 4), stride=(1, 2)),
            # SELayer(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_8_block1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=emb_size, kernel_size=(1, 16), stride=(1, 2)),
            # AttentionLayer(emb_size, reduction=2, mode=['SELayer'], kernel=(1, 3)),
            # SELayer(emb_size, 2),
            # CBAM(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_8_block2 = nn.Sequential(
            nn.Conv2d(in_channels=emb_size, out_channels=emb_size, kernel_size=(48, 1), stride=(1, 1)),
            # SELayer(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_8_block3 = nn.Sequential(
            nn.Conv2d(in_channels=emb_size, out_channels=emb_size, kernel_size=(1, 16), stride=(1, 2)),
            # SELayer(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_12_block1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=emb_size, kernel_size=(1, 48), stride=(1, 2)),
            # SELayer(emb_size, 2),
            # CBAM(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_12_block2 = nn.Sequential(
            nn.Conv2d(in_channels=emb_size, out_channels=emb_size, kernel_size=(48, 1), stride=(1, 1)),
            # SELayer(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.scale_12_block3 = nn.Sequential(
            nn.Conv2d(in_channels=emb_size, out_channels=emb_size, kernel_size=(1, 48), stride=(1, 2)),
            # SELayer(emb_size, 2),
            # CBAM(emb_size, 2),
            nn.BatchNorm2d(emb_size),
            nn.ELU(),
            nn.Dropout(self.dropout),
        )

        self.pooling = nn.AdaptiveAvgPool2d((1, 3))

        self.average_response = nn.Sequential(
            nn.AdaptiveAvgPool2d((48, 1)),
            nn.Flatten(),

        )

        self.cat_conv = nn.Sequential(
            nn.Conv2d(emb_size * 3, emb_size * 1, kernel_size=(1, 3), stride=1),
            nn.ELU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )

        self.linear = nn.Sequential(
            nn.Linear(emb_size + 48, (emb_size + 48) * 2),
            nn.ReLU(),
            nn.Linear((emb_size + 48) * 2, (emb_size + 48) * 1),
            nn.Linear((emb_size + 48) * 1, num_classes)
        )

    def forward(self, x):
        x = x.unsqueeze(1)
        x_copy = x.clone()

        x_average_response = self.average_response(x_copy)

        x_scale_4 = self.pooling(self.scale_4_block3(self.scale_4_block2(self.scale_4_block1(x_copy))))

        x_scale_8 = self.pooling(self.scale_8_block3(self.scale_8_block2(self.scale_8_block1(x_copy))))

        x_scale_12 = self.pooling(self.scale_12_block3(self.scale_12_block2(self.scale_12_block1(x_copy))))

        feature_cat = torch.cat([x_scale_4, x_scale_8, x_scale_12], dim=1)
        feature = self.cat_conv(feature_cat)

        feature = torch.cat([feature, x_average_response], dim=1)
        logits = self.linear(feature)

        return logits
