clc;

% im = imread('multi_face.jpg');
title('原图');
im = imread('test4.jpg');
% im = imread('one_face_h.jpg');
% im = imread('t2.jpg');
imshow(im);
[m,n,k] = size(im)        
result = zeros(m,n);

for i=1:m
	for j=1:n
           if im(i,j,1) > 95 && im(i,j,2) >40 && im(i,j,3)>20 ...
              && max([im(i,j,1),im(i,j,2),im(i,j,3)]) - min([im(i,j,1),im(i,j,2),im(i,j,3)])>15 ...
              && abs((im(i,j,1)-im(i,j,2)))>15 ...
              && im(i,j,1) > im(i,j,2) ...
              && im(i,j,1) > im(i,j,3)
			result(i,j)=1;      % 标记
		end
	end
end

figure;
imshow(result);
title('二值化结果');

%二值图像形态学处理
Se1=ones(5);
Se2=ones(9);
result=imerode(result,Se1); 
figure;
imshow(result);
title('腐蚀后的效果');
result=imdilate(result,Se2); 
figure;
imshow(result);
title('膨胀后的效果');

% 连通区域标记，默认8连通
% label就是标记连通区域后的结果，num为连通区域数
[label,num] = bwlabel(result,4);

box = regionprops(label,'BoundingBox');          % 获取标记框
centroid = regionprops(label,'Centroid');          % 获取标记中心
proportion = regionprops(label,'Extent');          % 同时在区域和其最小边界矩形中的像素比例

figure;
imshow(im), title('标记人脸');
hold on
for i = 1:num
    % 起始x，起始y，w，h
    bound = box(i).BoundingBox
    % 长 宽
    h = bound(4);
    w = bound(3);
    area = h * w;
    % 面积大于 1/200， 包含肤色的区域占矩形比例>0.6, 脸长/脸宽
    if area > m * n / 200 && proportion(i).Extent > 0.6 && h/w > 0.5
        rectangle('position', box(i).BoundingBox, 'edgecolor','r','LineWidth', 2);                          % 画框
        text(centroid(i,1).Centroid(1,1)-1,centroid(i,1).Centroid(1,2)-1, num2str(i),'Color', 'r')      % 标号
    end
end
