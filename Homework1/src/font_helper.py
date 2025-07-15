import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
import warnings

def setup_chinese_font():
    # 抑制字体警告
    warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*missing from font.*')
    warnings.filterwarnings('ignore', category=UserWarning, message='.*findfont.*')
    
    # 清除matplotlib字体缓存
    try:
        import shutil
        cache_dir = mpl.get_cachedir()
        font_cache = os.path.join(cache_dir, 'fontlist-v*.json')
        import glob
        for cache_file in glob.glob(font_cache):
            try:
                os.remove(cache_file)
            except:
                pass
        fm._rebuild()
    except:
        pass
    
    # 检查可用的中文字体
    available_fonts = [font.name for font in fm.fontManager.ttflist]
    
    # 常见的中文字体名称（按优先级排序）
    common_chinese_fonts = [
        'Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi', 'FangSong',
        'Microsoft JhengHei', 'PingFang SC', 'Heiti SC', 'STHeiti',
        'Arial Unicode MS', 'WenQuanYi Zen Hei'
    ]
    
    chinese_fonts = []
    for font_name in common_chinese_fonts:
        if font_name in available_fonts:
            chinese_fonts.append(font_name)
    
    # 设置字体
    if chinese_fonts:
        # 全局设置matplotlib字体
        mpl.rcParams['font.sans-serif'] = chinese_fonts
        mpl.rcParams['axes.unicode_minus'] = False  
        mpl.rcParams['font.family'] = 'sans-serif'
        
        # 也设置plt的参数
        plt.rcParams['font.sans-serif'] = chinese_fonts
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'sans-serif'
        
        print(f"已设置中文字体: {chinese_fonts[0]}")
        return chinese_fonts[0]
    else:
        # 如果没有找到中文字体，使用默认设置并提示
        fallback_fonts = ['Arial', 'DejaVu Sans', 'sans-serif']
        mpl.rcParams['font.sans-serif'] = fallback_fonts
        mpl.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.sans-serif'] = fallback_fonts
        plt.rcParams['axes.unicode_minus'] = False
        print("未找到中文字体，使用默认字体，中文可能显示为方块")
        return None 