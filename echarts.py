import os
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
import jieba


def test():
    df = pd.read_csv('data/data.csv')
    top_comments = df.nlargest(3, '评价数')

def cut_words(poem):
    stop_words = ['。', '，', '？','！','(', '（', '{', '、','）',')','【', '】', ';', ':', '：', '；', '“', '”', '《', '》', '……', '—', '——', '……', '·', '、', '‘', '’', '——', '———', '——']
    words = jieba.lcut(poem)
    filtered_words = [word for word in words if word not in stop_words]
    return filtered_words

# 生成评价数饼图
def create(filename):
    df = pd.read_csv(filename)

    # 进行数据清洗
    df = df.dropna()
    df.dropna(subset=['诗词名'], inplace=True)
    df.dropna(subset=['作者'], inplace=True)
    df.dropna(subset=['朝代'], inplace=True)
    df.dropna(subset=['古诗'], inplace=True)
    df.dropna(subset=['评价数'], inplace=True)
    df.dropna(subset=['评分'], inplace=True)


    #评价与评分统计
    top_authors_1 = df.sort_values('评价数', ascending=False).head(10).filter(items=['诗词名', '评价数','评分'])
    bar = (
        Bar(init_opts=opts.InitOpts(height="500px", width="50%"))
        .add_xaxis(top_authors_1['诗词名'].tolist())
        .add_yaxis('评价人数',top_authors_1['评价数'].tolist())
        .add_yaxis('评分', top_authors_1['评分'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="前10名诗词评分"),
            brush_opts=opts.BrushOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        )
    )

    # 朝代统计
    dynasty_counts = df['朝代'].value_counts()
    pie = (
        Pie(init_opts=opts.InitOpts(height="500px", width="50%"))
        .add('', data_pair=[(i, j) for i, j in zip(dynasty_counts.index.tolist(), dynasty_counts.values.tolist())])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="诗词朝代统计"),
            legend_opts=opts.LegendOpts(type_="scroll",pos_top='100px', pos_left="left", orient="vertical")
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    # 诗人创作作品数据
    authors = df['作者'].value_counts().head(10)
    bar_authors = (
        Bar(init_opts=opts.InitOpts(height="500px", width="50%"))
        .add_xaxis(authors.index.tolist())
        .add_yaxis('诗词数量', authors.values.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="前10名诗人创作数量")
        )
    )

    # 词云，古诗中出现最多的字
    df['分词'] = df['古诗'].apply(cut_words)
    words_series = df['分词'].explode()
    word_frequency = words_series.value_counts()
    words_s = word_frequency.head(200)
    word_cloud = (
        WordCloud(init_opts=opts.InitOpts(height="500px", width="50%"))
        .add(series_name='古诗词云统计', data_pair=[(i, j) for i, j in zip(words_s.index.tolist(), words_s.values.tolist())])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="古诗词云统计", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )
    page = Page(layout=Page.SimplePageLayout)
    page.add(bar, bar_authors, pie, word_cloud)
    page.render('html/index.html')

if __name__ == '__main__':
    create('data/data.csv')

