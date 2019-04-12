from django.shortcuts import render
# Create your views here.


class Pagination(object):

    def __init__(self,current_page,total_count,request,per_page_count=10,max_page_links=11):
        """
        封装分页相关数据
        :param current_page:   当前页
        :param total_count:     要分页的数据总条数
        :param per_page_count: 每页显示的数据条数
        :param max_page_links: 最多显示的页码个数
        :param num_pages:      计算总页数
        """

        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page <1:
            current_page = 1

        self.current_page = current_page
        self.total_count = total_count
        self.per_page_count = per_page_count


        # 计算总页数
        num_pages,tmp = divmod(total_count,per_page_count)
        if tmp:
            num_pages += 1
        self.num_pages = num_pages

        self.max_page_links = max_page_links     #  最大显示页码数    11
        self.max_page_links_half = int((self.max_page_links - 1) / 2) # 5

        # 请求信息字典
        import copy
        self.params=copy.deepcopy(request.GET)
        print("urlencode",self.params.urlencode())
        '''

        self.num_pages=100
        per_page=8


        current_page =1     [0:8]
        current_page =2     [8:16]
        current_page =3     [16:24]
                            [(current_page-1)*per_page:current_page*per_page ]

        '''


    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    def page_html(self):
        # 如果总页码 < 11个：
        if self.num_pages <= self.max_page_links:
            pager_start = 1
            pager_end = self.num_pages + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.max_page_links_half:
                pager_start = 1
                pager_end = self.max_page_links+1
            # 当前页大于5
            elif (self.current_page + self.max_page_links_half) > self.num_pages:
                    pager_start = self.num_pages-self.max_page_links+1
                    pager_end = self.num_pages + 1
            else:
                    pager_start = self.current_page - self.max_page_links_half
                    pager_end = self.current_page + self.max_page_links_half + 1

        page_html_list = []

        # 首页 上一页标签
        self.params["page"] = 1
        first_page = '<nav aria-label="Page navigation"><ul class="pagination"><li><a href="?%s">首页</a></li>' %(self.params.urlencode(),)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            self.params["page"] = self.current_page - 1
            prev_page = '<li><a href="?%s">上一页</a></li>' % (self.params.urlencode(),)

        page_html_list.append(prev_page)

        # 每一显示页码
        # self.params   {"page":"2","title__startswith":"py","c":"3"}
        for i in range(pager_start,pager_end):
                self.params["page"]=i
                if i == self.current_page:
                    temp = '<li class="active"><a href="?%s">%s</a></li>' % (self.params.urlencode(), i,)
                else:
                    temp = '<li><a href="?%s">%s</a></li>' % (self.params.urlencode(),i)

                page_html_list.append(temp)

        # 尾页 下一页
        self.params["page"] = self.current_page + 1
        if self.current_page >= self.num_pages:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?%s">下一页</a></li>' % (self.params.urlencode(),)
        page_html_list.append(next_page)

        self.params["page"]=self.num_pages
        last_page = '<li><a href="?%s">尾页</a></li></ul></nav>' % (self.params.urlencode())
        page_html_list.append(last_page)

        return ''.join(page_html_list)

