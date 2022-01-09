
clear
clc
%Define model path
addpath '/Users/nursimaunver/MemToolbox-master'
% Define data files path
Pilotdatafolder = '/Users/nursimaunver/2021-2022-FALL/Ori_DATA/';
% Get .csv files
d = dir([Pilotdatafolder, '/*.csv']);
sbj_no=[1 2 3 4 5 6 7 8 9 10 11 12 14];
%sbj_no = [1 2]

 
column_names_fit = ["degree_difference_baseNA", "degree_difference_distNA"];

%%
%for each participant

%preallocate
subj_base_dist= nan(180,4,length(sbj_no));
subj_mean_base_dist= nan(3,length(sbj_no))

sbj=0;
for subject= 1: length(sbj_no)
   
    sbj=sbj+1;
    
    subjectNumber = sbj_no(subject)
    
    T = readtable([Pilotdatafolder num2str(subjectNumber)]); % get subject data 
    
    baseNA_idx=find(~ismissing(T.degree_difference_baseNA)); % find the baseline condition trials
    
    base_NA=T.degree_difference_baseNA(baseNA_idx); %create a variable for baseline degree errors(NA-not absolute value)
    
    base_NA(base_NA > 180)= base_NA(base_NA >180) - 360; %correct for circularity
    base_NA(base_NA < - 180)= base_NA(base_NA < -180) + 360; %correct for circularity
    
    distNA_idx=find(~ismissing(T.degree_difference_distNA)); % find the distractor condition trials
    dist_NA=T.degree_difference_distNA(distNA_idx); %create a variable for distractor condition degree errors (NA-not absolute value)
    dist_NA(dist_NA >180)= dist_NA(dist_NA >180) - 360; %correct for circularity
    dist_NA(dist_NA < - 180)= dist_NA(dist_NA < -180) + 360; %correct for circularity
   
    baseT_idx=find(~ismissing(T.degree_difference_baseT)); % find the baseline condition trials- (T-absulute values)
    base_T=T.degree_difference_baseT(baseT_idx); %create a variable for baseline degree errors(T-absulute values)
    distT_idx=find(~ismissing(T.degree_difference_distT)); % find the distractor condition trials- (T-absulute values)
    dist_T=T.degree_difference_distT(distT_idx); %create a variable for distractor degree errors(T-absulute values)
    if any(subjectNumber == [1 2 3 4])
      dist_T= abs(dist_NA) %manually get the absolute values  
    end
        
   % base_dist= [base_NA dist_NA base_T dist_T];
    %subj_base_dist(:,:,subject)= base_dist;
   % base_mean= mean(base_T(90:180)) %take last half
   
    keyresp_idx=find(~ismissing(T.key_resp_dist_corr)); % find the distractor task key responses
    
    key_resp_corr=T.key_resp_dist_corr(keyresp_idx); %create a variable for key responses
   
    %subj_base_dist= [base_NA dist_NA base_T dist_T key_resp_corr];
    
    key_resp_acc =  mean(key_resp_corr); %overall accuracy for distractor task
    
   base_mean= mean(base_T) %baseline condition-mean error
   dist_mean=mean(dist_T) %distractor condition-mean error
   mean_base_dist = [base_mean; dist_mean; key_resp_acc] %combine base-dist variables
   subj_mean_base_dist(:,subject)=  mean_base_dist;
       %disp(subjectNumber)
       %disp(dist_NA)

       %fit_base(subject) = MemFit((base_NA)); %mixture modelling for baseline
       %fit_dist(subject) = MemFit((dist_NA)); %mixture modelling for distractor
    end

%% Save data
% FolderName = '/Users/nursimaunver/REAL_DATA/figures/';   % Your
% destination folder FigList = findobj(allchild(0), 'flat', 'Type',
% 'figure'); for iFig = 1:length(FigList)
%   FigHandle = FigList(iFig); FigName   = num2str(get(FigHandle,
%   'Number')); set(0, 'CurrentFigure', FigHandle);
%   savefig(fullfile(FolderName, [FigName '.fig']));
% end

%writematrix(subj_mean_base_dist,'ori811.xlsx')
