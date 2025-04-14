function main_plot_group_BLisEnd_P42()
% 画出群组平均的Happy Sad Neutral的响应，箱型图和条形图
% Bl is End的条件下，使用删trial方案4（中位数±3倍MAD）
load('TrialData_BLisEnd.mat');
load('Test_result_BLisEnd_P5.mat');
load('TrialRej_BLisEnd_P4.mat');
%% 任务 vs baseline
Correct_Index=3;  % 1=Raw; 2=FDR; 3=Bon
HB=Ch_Baseline{Correct_Index}; SB=Ch_Baseline{3+Correct_Index}; RB=Ch_Baseline{6+Correct_Index};
Plot_Ch=unique([HB,SB,RB]);  
ChC=length(Plot_Ch);
FigC=ceil(ChC/3);
cCh=0;
tbeg2=find(abs(tHRF+2)<2e-2);

    for iFig=1:FigC
        fgTotal=figure();
        set(gcf,'outerposition',get(0,'screensize'));
        axes('linewidth',1.5, 'FontSize',20);
        for iFigCh=1:3
            % 每张图画3Ch
            iP=iFigCh;  % 在第几行中画
            iLen=(iFigCh-1)*4+1;  % 画第几张图
            cCh=cCh+1;  pCh=Plot_Ch(cCh);

            % 每行
            % 第一个-曲线图-Happy trial
            subplot(3,4,iLen);  
            
            color_x=[255,0,0]/255;  % red
            color_y=[0,0,255]/255;  % blue
            % 0122 update 画部分通道
            Rj=Hrej_asac(:,pCh); Rj=logical(Rj);
            
            chavg_x=mean(ht(:,Rj,pCh),2)'*1e03;   % 沿被试平均
            % 岛津fNIRS的导出量纲为mMol，转化为uMol要乘以1000
            chavg_y=mean(ht_r(:,Rj,pCh),2)'*1e03;   
            chsem_x=std(ht(:,Rj,pCh),0,2)'*1e03/sqrt(size(ht(:,Rj,pCh),1));
            chsem_y=std(ht_r(:,Rj,pCh),0,2)'*1e03/sqrt(size(ht_r(:,Rj,pCh),1));

            sig_text=[];  % 判断哪两个条件之间有显著差异
            if ismember(pCh,HB)
                sig_text=[sig_text,'HB '];
            end
            if ismember(pCh,SB)
                sig_text=[sig_text,'SB '];
            end
            if ismember(pCh,RB)
                sig_text=[sig_text,'RB '];
            end 
            
            title({['Ch ',num2str(pCh),' Happy'],[' (BL Sig: ',sig_text,')']},'Interpreter','none');
            subPlot_HbOR_4_2(chavg_x,chavg_y,chsem_x,chsem_y,tHRF,fgTotal,color_x,color_y);   

            % 第二个-曲线图-Sad trial
            subplot(3,4,iLen+1);  
            % 0314 update 有些受试，通道和trial被拒绝了
            Rj=Srej_asac(:,pCh); Rj=logical(Rj);
            
            chavg_x=mean(st(:,Rj,pCh),2)'*1e03;   % 沿被试平均
            chavg_y=mean(st_r(:,Rj,pCh),2)'*1e03;   
            chsem_x=std(st(:,Rj,pCh),0,2)'*1e03/sqrt(size(st(:,Rj,pCh),1));
            chsem_y=std(st_r(:,Rj,pCh),0,2)'*1e03/sqrt(size(st(:,Rj,pCh),1));
            
            title('Sad');
            subPlot_HbOR_4_2(chavg_x,chavg_y,chsem_x,chsem_y,tHRF,fgTotal,color_x,color_y);   

            % 第三个-曲线图-Neurtral trial
            subplot(3,4,iLen+2);  
            % 0314 update 有些受试，通道和trial被拒绝了
            Rj=Nrej_asac(:,pCh); Rj=logical(Rj);
            
            chavg_x=mean(rt(:,Rj,pCh),2)'*1e03;   % 沿被试平均
            chavg_y=mean(rt_r(:,Rj,pCh),2)'*1e03;   
            chsem_x=std(rt(:,Rj,pCh),0,2)'*1e03/sqrt(size(rt(:,Rj,pCh),1));
            chsem_y=std(rt_r(:,Rj,pCh),0,2)'*1e03/sqrt(size(rt(:,Rj,pCh),1));
            
            title('Neutral');
            subPlot_HbOR_4_2(chavg_x,chavg_y,chsem_x,chsem_y,tHRF,fgTotal,color_x,color_y);  
            
            if cCh==ChC
                break;
            end
        end
        
        figtitle=['End_Baseline_Fig_',num2str(iFig)];
        savetitle=['fig_P42\',figtitle];
        
        print(savetitle,'-dtiff');
        close(gcf);
    end

%% 条件间显著性检验
% 计算画的figure数
% Correct_Index=1;  % 1=Raw; 2=FDR; 3=Bon
% HB=Ch_BetwCond{Correct_Index}; SB=Ch_BetwCond{3+Correct_Index}; RB=Ch_BetwCond{6+Correct_Index};
% Plot_Ch=unique([HB,SB,RB]);  
% ChC=length(Plot_Ch);
% FigC=ceil(ChC/3);
% cCh=0;
% 
%     for iFig=1:FigC
%         fgTotal=figure();
%         set(gcf,'outerposition',get(0,'screensize'));
%         axes('linewidth',1.5, 'FontSize',20);
%         for iFigCh=1:3
%             % 每张图画3Ch
%             iP=iFigCh;  % 在第几行中画
%             iLen=(iFigCh-1)*4+1;  % 画第几张图
%             cCh=cCh+1;  pCh=Plot_Ch(cCh);
% 
%             % 曲线图
%             subplot(3,4,iLen);  % 曲线   
%             Rjh=Hrej_asac(:,pCh); Rjh=logical(Rjh);
%             Rjs=Srej_asac(:,pCh); Rjs=logical(Rjs);
%             Rjn=Nrej_asac(:,pCh); Rjn=logical(Rjn);
%             
%             chavg_x=mean(ht(:,Rjh,pCh),2)'*1e03;   % 沿被试平均
%             chavg_y=mean(st(:,Rjs,pCh),2)'*1e03;  
%             chavg_z=mean(rt(:,Rjn,pCh),2)'*1e03;  
%             chsem_x=std(ht(:,Rjh,pCh),0,2)'*1e03/sqrt(size(ht(:,Rjh,pCh),1));
%             chsem_y=std(st(:,Rjs,pCh),0,2)'*1e03/sqrt(size(st(:,Rjs,pCh),1));
%             chsem_z=std(rt(:,Rjn,pCh),0,2)'*1e03/sqrt(size(rt(:,Rjn,pCh),1));
% 
%             color_x=[255,31,255]/255;
%             color_y=[186,135,11]/255;
% 
%             title(['Ch ',num2str(pCh)]);
%             subPlot_FcXYZ(chavg_x,chavg_y,chavg_z,chsem_x,chsem_y,chsem_z,tHRF,fgTotal,color_x,color_y);   
% 
%             % 箱型图
%             subplot(3,4,iLen+1);  
% 
%             htm=mean(ht(:,Rjh,pCh),1)'*1e03; % 沿时间平均
%             stm=mean(st(:,Rjs,pCh),1)'*1e03; 
%             rtm=mean(rt(:,Rjn,pCh),1)'*1e03; 
%             boxplot([htm,stm,rtm]); 
%             set(gca, 'fontsize',16); 
%             xticklabels({'happy','sad','rest'});
% 
%             % 条形图
%             subplot(3,4,iLen+2);  
% 
%             htm=mean(ht(:,Rjh,pCh),1)'*1e03; % 沿时间平均
%             stm=mean(st(:,Rjs,pCh),1)'*1e03; 
%             rtm=mean(rt(:,Rjn,pCh),1)'*1e03; 
%             bar(Mean_state_hbo_oc(pCh,:));  hold on
%             errorbar(Mean_state_hbo_oc(pCh,:),Sem_state_hbo_oc(pCh,:),'o');
%             set(gca, 'fontsize',16);  hold off;
%             xticklabels({'happy','sad','neutral'});
%             
%             sig_text=[];  % 判断哪两个条件之间有显著差异
%             if ismember(pCh,HB)
%                 sig_text=[sig_text,'HN '];
%             end
%             if ismember(pCh,SB)
%                 sig_text=[sig_text,'SN '];
%             end
%             if ismember(pCh,RB)
%                 sig_text=[sig_text,'HS '];
%             end
%             title(sig_text);
%             
%             if cCh==ChC
%                 break;
%             end
%         end
%         
%         figtitle=['End_Cond_Fig_',num2str(iFig)];
%         savetitle=['fig_P42\',figtitle];
%         
%         print(savetitle,'-dtiff');
%         close(gcf);
%     end



end
