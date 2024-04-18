# from cutecharts.charts import Pie
# from cutecharts.components import Page
# from cutecharts.faker import Faker


# def pie_base() -> Pie:
#     chart = Pie("Pie", width='1024px', height='1024px')
#     chart.set_options(
#         labels=["positive", "neutral", "negative"],
#         inner_radius=0,
#         legend_pos="upRight",
#     )
#     print(chart._switch_pos("upRight"))
#     chart.add_series([1000, 2000, 300])
#     return chart


# pie_base().render(template_name='basic_local.html')


import matplotlib.pyplot as plt

import matplotlib as mpl

with plt.xkcd():
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels)

plt.show()




