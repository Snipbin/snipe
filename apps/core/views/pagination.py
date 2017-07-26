from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.urls import reverse
from django.views import View
from urllib.parse import urlencode

from apps.core.utils import VIEW_PAGE_SIZE


class PaginationView(View):
    paginator: Paginator = None
    page_name = 'page'
    page: Page = None

    def get_page(self, object_list):
        self.paginator = SnipePaginator(object_list)

        inquired_page = self.request.GET.get(self.page_name)
        try:
            page = self.paginator.page(inquired_page)
        except (PageNotAnInteger, EmptyPage):
            page = self.paginator.page(1)

        self.page = page
        return self.page

    def update_pagination_context(self, context: dict, page: Page = None):
        if not page:
            page = self.page

        has_next = page.has_next()
        has_previous = page.has_previous()

        next_page_number = page.next_page_number() if has_next else -1
        previous_page_number = page.previous_page_number() if has_previous else -1

        next_query_dict = self.request.GET.dict()
        previous_query_dict = self.request.GET.dict()

        next_query_dict.update({
            self.page_name: next_page_number,
        })

        previous_query_dict.update({
            self.page_name: previous_page_number,
        })

        base_url = reverse('snippet:discover')
        next_url = f'{base_url}?{urlencode(next_query_dict)}'
        previous_url = f'{base_url}?{urlencode(previous_query_dict)}'

        context.update({
            'page_name': self.page_name,
            'has_next': has_next,
            'has_previous': has_previous,
            'next_disabled': '' if has_next else 'disabled',
            'previous_disabled': '' if has_previous else 'disabled',
            'next_url': next_url,
            'previous_url': previous_url,
        })

        return context


class SnipePaginator(Paginator):

    def __init__(self, object_list, per_page=VIEW_PAGE_SIZE, orphans=0,
                 allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans=orphans, allow_empty_first_page=allow_empty_first_page)
