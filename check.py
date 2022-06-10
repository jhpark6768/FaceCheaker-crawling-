import os
import pandas as pd
import cv2   # OpenCV
from skimage import measure
from skimage.metrics import structural_similarity as ssim
import shutil


photo_list = []

for f in os.listdir('C:/Users/82107/Desktop/python/helmet'):
    if 'jpg' in f:
        photo_list.append(f)

photo_size = list(map(lambda x: os.path.getsize('C:/Users/82107/Desktop/python/helmet' + '/' + x), photo_list))

fsp = pd.DataFrame({'filename_raw':photo_list, 'size':photo_size})

print('사진의 갯수 :', len(fsp))

psvc = pd.DataFrame({'size':fsp['size'].value_counts().index, 'size_counts_nsn':fsp['size'].value_counts().values})
fsp_nsn = pd.merge(fsp, psvc, how = 'left', on = 'size')
print('중복 사이즈의 갯수 :', len(psvc[psvc['size_counts_nsn']>1]))
print(psvc[psvc['size_counts_nsn']>1])

delete = []


for i in range(len(psvc)):
    
    # 중복된 크기(size)가 있는 경우
    if psvc['size_counts_nsn'][i] == 2:
        
        # 그 크기에 해당하는 사진을 불러온다. 
        temp = fsp_nsn[fsp_nsn['size']==psvc['size'][i]].reset_index(drop = True).sort_values(['filename_raw'])
        
        # 사진 읽기
        imageA = cv2.imread('C:/Users/82107/Desktop/python/helmet/'+temp['filename_raw'][0])
        imageB = cv2.imread('C:/Users/82107/Desktop/python/helmet/'+temp['filename_raw'][1])
        
        # 이미지를 grayscale로 변환
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        
        # 이미지의 구조가 같다면 이미지 비교
        if len(grayA)==len(grayB):
            (score, diff) = ssim(grayA, grayB, full=True)
            
            # 차이가 없다면 하나는 delete에 넣어주기
            if score == 1:
                delete.append(temp['filename_raw'][1])
            
            # 구조가 같지만 차이가 존재한다면 직접 확인하기     
            else:
                print('확인해보시오! : ', temp['filename_raw'][0], '/', temp['filename_raw'][1], f'(score : {score})')

delete = delete + list(fsp[~fsp['filename_raw'].isin(fsp_nsn['filename_raw'])]['filename_raw'])

print('삭제할 목록 :', len(delete))

# result : 처음(fsp)데이터에서 - delete를 제외한 것
result = list(fsp[~fsp['filename_raw'].isin(delete)]['filename_raw'])

print('남길 목록 : ', len(result))

for i in result:
    shutil.move('C:/Users/82107/Desktop/python/helmet/'+i, 'C:/Users/82107/Desktop/python/helmet/Result')
    
for i in delete:
    shutil.move('C:/Users/82107/Desktop/python/helmet/'+i, 'C:/Users/82107/Desktop/python/helmet/Delete')