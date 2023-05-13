
pakages = '''
scrapy,openpyxl
'''
def setup():
    import os
    os.system(f"pip install {' '.join(pakages.strip().split(','))}")

if __name__ == '__main__':
    pass