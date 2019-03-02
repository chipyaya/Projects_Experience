SET level=%1
SET filename=%2
SET centerX=%3
SET centerY=%4
SET /a anotherX=centerX-430

SET convert_cmd="C:\Windows\System32\ImageMagick-7.0.1-1-portable-Q16-x64\convert.exe"
SET img_path=.\kinect_code\NTUAF-Recognize\NTUAF-Recognize\images\
SET jpeg_path=%img_path%%filename%.jpeg
SET png_path=%img_path%%filename%.png
SET person_path=%img_path%person.png
SET cir="circle %centerX%,%centerY% %anotherX%,%centerY%"
%convert_cmd% %jpeg_path% %png_path%

%convert_cmd% -size 1290x1080 xc:none -fill %png_path% -draw %cir% %person_path% 

SET /a x=700-%centerX%
SET /a y=540-%centerY%
%convert_cmd% .\public\img\win_loo\win_loo_%level%.png %person_path% -geometry +%x%+%y% -composite .\public\img\composite.png


