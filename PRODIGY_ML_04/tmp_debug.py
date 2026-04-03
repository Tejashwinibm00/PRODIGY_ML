import os
DATA_DIR = 'C:/Users/HP/Downloads/Hand gesture/leapGestRecog'
print('exists', os.path.exists(DATA_DIR))
count=0
for root, dirs, files in os.walk(DATA_DIR):
    print('ROOT', root)
    print('  DIRS', dirs[:5])
    print('  FILES', files[:5])
    count += 1
    if count > 20:
        break
print('done')
