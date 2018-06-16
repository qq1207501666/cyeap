import math


def revise_page_num(page_num, page_size, record_count):
    """
     修正页码
     :param page_num: 页码
     :param page_size: 每页的记录数
     :param record_count: 总记录数
     :return: 一个正确的页码
    """
    page_num = int(page_num)
    page_size = int(page_size)
    record_count = int(record_count)
    total_page = math.ceil(record_count / page_size)  # 计算总页数
    page_num = 1 if page_num < 1 else page_num  # 如果页码小于1 则 = 1
    page_num = total_page if page_num > total_page else page_num  # 如果页码大于总页数 则 = 总页数
    return page_num


def get_page_range(page_num, page_size, record_count, plus_num=4):
    """
    返回一个良好的分页范围
    根据当前的页码计算一个页码范围,优化页数过多,页面无法展示的问题
    这样,就算总页数有100页,也最大只会显示9页(这是因为plus_num = 4)
        最大显示页数 = plus_num * 2 + 1
    一般情况下,当前页会在中间位置,例如:当前页为第11页,页面显示
        <上一页 7 8 9 10 [11] 12 13 14 15 下一页>
    :param page_num: 当前页码
    :param page_size: 每页显示的记录数
    :param record_count: 总记录数
    :param plus_num: 增量页数
    :return: range(first_page,last_page) 页码优化范围
    """
    total_page = math.ceil(record_count / page_size)  # 计算总页数
    # 计算左边第一个的页码,默认为第1页
    first_page = 1
    if page_num > 5:
        first_page = page_num - plus_num
    if first_page > total_page - plus_num:
        first_page = total_page - plus_num
    if first_page < 1:
        first_page = 1
    # 计算右边最后一个的页码,默认为第9页
    last_page = 9
    if page_num > plus_num:
        last_page = page_num + plus_num
    if last_page > total_page:
        last_page = total_page
    if total_page < 10:
        first_page = 1
        last_page = total_page
    return range(first_page, last_page + 1)


def page_html(page_num, page_size, record_count, plus_num=4):
    """
    :param page_num: 当前页码
    :param page_size: 每页显示的记录数
    :param record_count: 总记录数
    :param plus_num: 增量页数
    :return: html ul 分页代码
    """
    page_range = get_page_range(page_num, page_size, record_count, plus_num)
    html = """
        <ul class="pagination">
        <li>
            <a id="previous_page" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>
        </li>
        """
    for i in page_range:
        active_css = ""
        if page_num == i:
            active_css = "class='active'"
        html += """<li %s ><a class="page_num" href = '#' >%s</a></li>""" % (active_css, i)
    else:
        html += """
            <li>
                <a id="next_page" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>
            </li>
            </ul>
            """
    return html
