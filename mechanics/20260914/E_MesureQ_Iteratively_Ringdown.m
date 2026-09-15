clear QArray
for i=1:2
   RingdownFitAndSave

   txt=['Q = ' num2str(Q,'%10.3e')];
   
   QArray(i)=Q;
   pause(1)
end

Qmean=mean(QArray)
Qstd=std(QArray)

txt=['Q = ' num2str(Qmean,'%10.3e') '\pm' num2str(Qstd,'%10.1e')]
    