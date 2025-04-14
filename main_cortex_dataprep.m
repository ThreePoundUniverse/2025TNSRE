function main_cortex_dataprep()
    % bonfe检验结果投影到皮层
    load('groupResults.mat');
    load('Test_result_BLisEnd_P5.mat');  % vs Baseline画FDR校正后的，条件间画无校正的
    
    t_end=length(group.procResult.tHRF);
    
    %% vs baseline Mean Conc 
    % 计算mean的阈值
    % （1）只显示少部分通道
    % histogram(abs(Mean_state_hbo_oc(:,1)));
    % （2）显著通道必须全部显示
%     i1=mapp_Baseline(:,2)~=0;  c1=Mean_state_hbo_oc(i1,1);
%     i2=mapp_Baseline(:,5)~=0;  c2=Mean_state_hbo_oc(i2,2);  
    cThres=0.5;  % conc threshold 
    
    % HbO 放Left  
    Left=1:25; Right=24:48;
    for iTP=1:t_end
        hConc_pow=find(abs(Mean_state_hbo_oc(:,1))>cThres);  % happy conc - powerful(强的) channel
        hl=intersect(Left,hConc_pow); hr=setdiff(1:48,hl);   % 画left强Ch，其他（left弱&right）通道屏蔽掉
        sConc_pow=find(abs(Mean_state_hbo_oc(:,2))>cThres);
        sl=intersect(Left,sConc_pow); sr=setdiff(1:48,sl);
 
        group.procResult.dcAvg(iTP,1,hl,1)=Mean_state_hbo_oc(hl,1);  % Happy - 左边的强Chan
        group.procResult.dcAvg(iTP,1,hr,1)=0;  
        group.procResult.dcAvg(iTP,1,sl,2)=Mean_state_hbo_oc(sl,2);  % Sad
        group.procResult.dcAvg(iTP,1,sr,2)=0;  
    end
    
    % HbR 放 Right 
    for iTP=1:t_end
        hConc_pow=find(abs(Mean_state_hbo_oc(:,1))>0.3);  % happy conc - powerful(强的) channel
        hr=intersect(Right,hConc_pow); hl=setdiff(1:48,hr);   
        sConc_pow=find(abs(Mean_state_hbo_oc(:,2))>0.3);
        sr=intersect(Right,sConc_pow); sl=setdiff(1:48,sr);
       
        group.procResult.dcAvg(iTP,2,hl,1)=0;  % Happy - 右边的强Chan
        group.procResult.dcAvg(iTP,2,hr,1)=Mean_state_hbo_oc(hr,1);  
        group.procResult.dcAvg(iTP,2,sl,2)=0;  % Sad
        group.procResult.dcAvg(iTP,2,sr,2)=Mean_state_hbo_oc(sr,2);  
    end
    
    % vs baseline p-value 
    % 放HbO, 这是FDR校正后的，Left 放HbO
    for iTP=1:t_end
        group.procResult.dcAvg(iTP,1,Left,3)=mapp_Baseline(Left,2);  % Happy
        group.procResult.dcAvg(iTP,1,Right,3)=0;
        group.procResult.dcAvg(iTP,1,Left,4)=mapp_Baseline(Left,5);  % Sad
        group.procResult.dcAvg(iTP,1,Right,4)=0;
    end
    
    % Right 放HbR
    for iTP=1:t_end
        group.procResult.dcAvg(iTP,2,Right,3)=mapp_Baseline(Right,2);  % Happy
        group.procResult.dcAvg(iTP,2,Left,3)=0;
        group.procResult.dcAvg(iTP,2,Right,4)=mapp_Baseline(Right,5);  % Sad
        group.procResult.dcAvg(iTP,2,Left,4)=0;
    end
    
    
    % 条件间比较 画无校正的
    Mean_betwcond(:,1)=Mean_state_hbo_oc(:,1)-Mean_state_hbo_oc(:,2);  % HS
    
     % 【7-9】Mean 
    % HbO 放Left  
    Left=1:25; Right=24:48;
    for iTP=1:t_end
        nConc_pow=find(abs(Mean_betwcond(:,1))>cThres);
        nl=intersect(Left,nConc_pow); nr=setdiff(1:48,nl);
        group.procResult.dcAvg(iTP,1,nl,5)=Mean_betwcond(nl,1);  % HS
        group.procResult.dcAvg(iTP,1,nr,5)=0;  
    end
    
    % HbR 放 Right 
    for iTP=1:t_end
        nConc_pow=find(abs(Mean_betwcond(:,1))>0.3);
        nr=intersect(Right,nConc_pow); nl=setdiff(1:48,nr);
        group.procResult.dcAvg(iTP,2,nl,5)=0;  % Neutral
        group.procResult.dcAvg(iTP,2,nr,5)=Mean_betwcond(nr,1);  
    end
    
    % 左脑放HbO-第二个维度
    for iTP=1:t_end
        group.procResult.dcAvg(iTP,1,Left,6)=mapp_BetwCond(Left,2);  % Happy vs Sad
        group.procResult.dcAvg(iTP,1,Right,6)=0;
    end
    % 右脑放HbR
    for iTP=1:t_end
         group.procResult.dcAvg(iTP,2,Right,6)=mapp_BetwCond(Right,2);  % Happy vs Sad
        group.procResult.dcAvg(iTP,2,Left,6)=0;
    end
    
    % 除了这6条以外的都删掉
    if size(group.procResult.dcAvg,4)>6
        group.procResult.dcAvg(:,:,:,7:size(group.procResult.dcAvg,4))=[];
    end
        
    save('groupResults_BLisEnd_TrejP32.mat','group');
    save('groupResults.mat','group');
end