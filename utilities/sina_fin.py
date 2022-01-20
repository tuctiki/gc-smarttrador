import re
import urllib.request

SINA_BASE_INFO_API_TEMPLATE = "https://hq.sinajs.cn/list=%s"
SINA_BASE_INFO_RESPONSE_PARSER = re.compile(r'(?<=")[^\']+(?=")')


def translate_quote(quote):
    if quote.startswith('of'):
        quote_prefix = "%s"
    elif len(quote) < 6:
        quote_prefix = "hk%s"
    elif quote.startswith('60'):
        quote_prefix = "sh%s"
    else:
        quote_prefix = "sz%s"
    return quote_prefix % quote


def compose_request_url(sina_quote):
    return SINA_BASE_INFO_API_TEMPLATE % sina_quote


def get_price(quote):
    # translate original quote to application specific quote
    application_quote = translate_quote(quote)
    response = get_quote_info(application_quote)
    if application_quote.startswith("hk"):
        current_value = response[6]
        # a workaround for getting 0 in the weekend, try with price of the last day
        if float(current_value) == 0:
            current_value = response[3]
        return current_value
    elif application_quote.startswith("of"):
        return response[1]
    elif application_quote.startswith("sz") or application_quote.startswith("sh"):
        current_value = response[3]
        if float(current_value) == 0:
            current_value = response[2]
        return current_value
    return response[3]


def get_name(quote):
    # translate original quote to application specific quote
    application_quote = translate_quote(quote)
    response = get_quote_info(application_quote)
    # extract current price from response
    return response[0]


def get_quote_info(quote):
    # compose request api url
    request_api_url = compose_request_url(quote)
    # get response body
    req = urllib.request.Request(request_api_url)
    req.add_header('Referer', 'https://finance.sina.cn/')
    # print req.headers['content-type']
    response = str(urllib.request.urlopen(req).read(), encoding="GBK")
    # extract info
    m = SINA_BASE_INFO_RESPONSE_PARSER.search(response)
    if m:
        group = re.split(r',+', m.group())
    else:
        group = ""
    return group
