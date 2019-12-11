% im0 = imread('test1.jpg');
% im1 = rgb2gray(im0);
im1 = imread('Fig0308(a)(fractured_spine).tif');
im = uint8(im1);
% 做运算时转换为double保证精度
im = im2double(im);
% imshow(im);
[x, y] = size(im);

after = im
% gamma 取不同的值
gamma0 = [0.1, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 1.6];
for n = 1:8
    subplot(2,4,n)
    for i = 1:x
        for j = 1:y
            after(i, j) = im(i,j)^gamma0(n);
        end
    end
    imshow(after)
    title(['gamma = ', num2str(gamma0(n))]);  
end



        