ScrapePreventionChildProtection = "sgdhu0zJqMNwJMptmKK7,D2tD8NvxzqaOYTTsMyLF,GxE9O06PhZ76l26h3jWk,tbgpTwdRRrjPVatmRst0,Tjg05gCHSyVzwbdrDswZ,RYbgX8HE2RdJlucai4je,G68x6cY2lZlQmU1ndOEV,9gOCaOEkmcvwLFfgVLHb,PPJkVEbvB1WWx9YTUgIb,qTZGIfrqIv8FLSunL93A"


def getkey():
    with open('secret.key','r') as kf:
        return kf.read().strip()
def opentab(url):
    webbrowser.open(url)
def new(filename,author):
    post = {'author':author,'content':''}
    return post
def load(filename):
    post = frontmatter.load(filename)
    #post.content, post['enc']
    return post
def dump(content,filename):
    with open(filename,'w+') as file:
        frontmatter.dump(content, file)
def args():
    """get the filename from arguments"""
    return sys.argv[1]
