import sublime
import sublime_plugin


class LastEditCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        lastEditLineLength = len(RecordIntputRegion.editLineList)
        index = RecordIntputRegion.current_index
        print("lastEditLineLength", lastEditLineLength)
        print('index ', index)
        if lastEditLineLength > 0 and index > 0:
            lastEditLine = RecordIntputRegion.editLineList[index-1]
            RecordIntputRegion.current_index = RecordIntputRegion.current_index - 1
            print(lastEditLine)
            jumpLastPoint(jumpLastView(lastEditLine[0]), lastEditLine[1], 0)

class NextEditCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        lastEditLineLength = len(RecordIntputRegion.editLineList)
        index = RecordIntputRegion.current_index
        print("lastEditLineLength", lastEditLineLength)
        print('index ', index)
        if lastEditLineLength > 0 and index < lastEditLineLength-1:
            lastEditLine = RecordIntputRegion.editLineList[index+1]
            RecordIntputRegion.current_index = RecordIntputRegion.current_index + 1
            print(lastEditLine)
            jumpLastPoint(jumpLastView(lastEditLine[0]), lastEditLine[1], 0)
        



class SwitchEditViewCommand(sublime_plugin.TextCommand):

    def run(self, edit, way="left"):
        if way == "left":
            lastView = RecordIntputRegion.editView.pop()
            RecordIntputRegion.editView.insert(0, lastView)
            if lastView == self.view.id():
                lastView = RecordIntputRegion.editView.pop()
                RecordIntputRegion.editView.insert(0, lastView)
        else:
            lastView = RecordIntputRegion.editView.pop(0)
            RecordIntputRegion.editView.append(lastView)
            if lastView == self.view.id():
                lastView = RecordIntputRegion.editView.pop(0)
                RecordIntputRegion.editView.append(lastView)
        jumpLastView(lastView)


def jumpLastView(lastView):
    lastViewObj = None
    lastWindow = None
    for window in sublime.windows():
        for view in window.views():
            if lastView == view.id():
                lastViewObj = view
                lastWindow = window
                pass
    print("jumpLastView ", lastWindow)
    if lastWindow:
        lastGroup, _ = lastWindow.get_view_index(lastViewObj)
        lastWindow.focus_group(lastGroup)

        lastWindow.focus_view(lastViewObj)

    return lastViewObj


def jumpLastPoint(lastViewObj, lastViewLine, lastViewCol):
    if lastViewObj:
        print("last point ", lastViewLine, lastViewCol)
        pt = lastViewObj.text_point(lastViewLine, lastViewCol)
        print("pt ", pt)
        lastViewObj.sel().clear()

        lastViewObj.sel().add(sublime.Region(pt))

        lastViewObj.show(pt)


def getLastEditLine():
    lastView = None
    lastViewLine = None
    lastViewLen = len(RecordIntputRegion.lastView)
    print("getLastEditLine all last views ", RecordIntputRegion.lastView)
    if lastViewLen > 0:
        viewsCount = lastViewLen - 1
        lastView = RecordIntputRegion.lastView[viewsCount]
        lastViewPosKey = str(lastView) + ":" + str(viewsCount)
        if len(RecordIntputRegion.lastLine[lastViewPosKey]) == 0:
            RecordIntputRegion.lastView.pop()
            viewsCount = lastViewLen - 1
            lastView = RecordIntputRegion.lastView[viewsCount]
            lastViewPosKey = str(lastView) + ":" + str(viewsCount)
        lastViewLine = RecordIntputRegion.lastLine[lastViewPosKey].pop()
    return lastView, lastViewLine

def getNextEditLine():
    lastView = None
    lastViewLine = None
    lastViewLen = len(RecordIntputRegion.lastView)
    print("getLastEditLine all last views ", RecordIntputRegion.lastView)
    if lastViewLen > 0:
        viewsCount = lastViewLen - 1
        lastView = RecordIntputRegion.lastView[viewsCount]
        lastViewPosKey = str(lastView) + ":" + str(viewsCount)
        if len(RecordIntputRegion.lastLine[lastViewPosKey]) == 0:
            RecordIntputRegion.lastView.pop()
            viewsCount = lastViewLen - 1
            lastView = RecordIntputRegion.lastView[viewsCount]
            lastViewPosKey = str(lastView) + ":" + str(viewsCount)
        lastViewLine = RecordIntputRegion.lastLine[lastViewPosKey].pop()
    return lastView, lastViewLine

class RecordIntputRegion(sublime_plugin.EventListener):
    editLine = {}
    lastLine = {}
    lastView = []
    editView = []

    editLineList = []
    current_index = -1

    def on_modified(self, view):
        sel = view.sel()[0]

        curr_view = view.id()
        last_line, last_col = view.rowcol(sel.begin())

        if view.id() == 4:
            return
        lastViewPos = len(RecordIntputRegion.lastView) - 1
        lastSwitchViewPos = len(RecordIntputRegion.editView) - 1

        if lastViewPos == -1:
            RecordIntputRegion.lastView.append(curr_view)
            lastViewPos += 1
            pass

        if not RecordIntputRegion.lastView[lastViewPos] is curr_view:
            RecordIntputRegion.lastView.append(curr_view)
            lastViewPos += 1
        if lastSwitchViewPos == -1:
            RecordIntputRegion.editView.append(curr_view)
            lastSwitchViewPos += 1
            pass

        if not RecordIntputRegion.editView[lastSwitchViewPos] is curr_view:
            RecordIntputRegion.editView.append(curr_view)

        viewPosKey = str(curr_view) + ":" + str(lastViewPos)
        if not RecordIntputRegion.lastLine.get(viewPosKey):
            RecordIntputRegion.lastLine[viewPosKey] = []
            pass

        lastLinePos = len(RecordIntputRegion.lastLine[viewPosKey]) - 1

        if lastLinePos == -1:
            RecordIntputRegion.lastLine[viewPosKey].append(last_line)
            lastLinePos += 1

        if not RecordIntputRegion.lastLine[viewPosKey][lastLinePos] is last_line:
            RecordIntputRegion.lastLine[viewPosKey].append(last_line)
            pass
        if not RecordIntputRegion.editLine.get(curr_view):
            RecordIntputRegion.editLine[curr_view] = {}
            pass
        RecordIntputRegion.editLine[curr_view][last_line] = last_col

        index = RecordIntputRegion.current_index
        print('start ', RecordIntputRegion.current_index, ' ', RecordIntputRegion.editLineList)
        if index > -1:
            for i in RecordIntputRegion.editLineList:
                if i==[curr_view, last_line]:
                    RecordIntputRegion.editLineList.remove(i)
        if len(RecordIntputRegion.editLineList) > 100:
            RecordIntputRegion.editLineList.pop(0)
        RecordIntputRegion.editLineList.append([curr_view, last_line])
        RecordIntputRegion.current_index = len(RecordIntputRegion.editLineList)-1 
        print('end', RecordIntputRegion.current_index, ' ', RecordIntputRegion.editLineList)
