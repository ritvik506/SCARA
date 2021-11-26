close all;
clear;
clc;
l1=15;
l2=10;
d2=2;%Thickness of link
view(-37.5,30);hold on
theta1=linspace(-30,30,10);
theta2=linspace(-30,30,10);
d3=linspace(0,20,10);

Base=[0,0,18,0];
T00=transd(Base(1),Base(2),Base(3),Base(4));
plotTransd(T00)

for i=1:10
for j=1:10
for k=1:10

DH = [  0, 0, 0, theta1(i);
        0, l1, d2, theta2(j);
        0, l2, -d3(k), 0; ];


T01 = transd(DH(1,1),DH(1,2),DH(1,3),DH(1,4));
T01=T00*T01;
plotTransd(T01)
T12=transd(DH(2,1),DH(2,2),DH(2,3),DH(2,4));
T02=T01*T12;
plotTransd(T02)
T23=transd(DH(3,1),DH(3,2),DH(3,3),DH(3,4));
T03=T02*T23;
plotTransd(T03)
axis([-10,40,-20,20,0,25]);
pause(0.000001)

end
end
end
%%
%Symbolic FK
close all;
clear;
clc;
l1=15;
l2=10;
d2=2;%Thickness of link
syms theta1 theta2 d3

Base=[0,0,18,0];
T00=transd(Base(1),Base(2),Base(3),Base(4));

DH = [  0, 0, 0, theta1;
        0, l1, d2, theta2;
        0, l2, -d3, 0; ];
   
T01 = transd(DH(1,1),DH(1,2),DH(1,3),DH(1,4));
T01=T00*T01;

T12=transd(DH(2,1),DH(2,2),DH(2,3),DH(2,4));
T02=T01*T12;

T23=transd(DH(3,1),DH(3,2),DH(3,3),DH(3,4));
T03=T02*T23



