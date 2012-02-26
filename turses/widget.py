###############################################################################
#                               coding=utf-8                                  #
#           Copyright (c) 2012 Nicolas Paris and Alejandro Gómez.             #
#       Licensed under the GPL License. See LICENSE.txt for full details.     #
###############################################################################

import urwid


class Tabs(urwid.WidgetWrap):
    """
    TODO
    """

    def __init__(self, tabs=[]):
        """Creates tabs with the names given in `tabs`."""
        self.tabs = tabs
        if tabs:
            self.active_index = 0
        else:
            self.active_index = -1
        text = self._create_text()
        urwid.WidgetWrap.__init__(self, urwid.Text(text))

    def _is_valid_index(self, index):
        return index >= 0 and index < len(self.tabs)

    def _create_text(self):
        """Creates the text that is rendered as the tab list."""
        text = []
        for i, tab in enumerate(self.tabs):
            tab = tab + ' '
            if i == self.active_index:
                text.append(('active_tab', tab))
            else:
                text.append(('inactive_tab', tab))
        return text

    def _update_text(self):
        text = self._create_text()
        self._w.set_text(text)

    def append_tab(self, tab):
        self.tabs.append(tab)
        self._update_text()

    def delete_current_tab(self):
        del self.tabs[self.active_index]
        self._update_text()

    def _set_active_tab(self, pos):
        self.active_index = pos
        self._update_text()

    def activate_previous(self):
        next_index = self.active_index - 1
        if self._is_valid_index(next_index):
            self._set_active_tab(next_index)

    def activate_next(self):
        next_index = self.active_index + 1
        if self._is_valid_index(next_index):
            self._set_active_tab(next_index)


#TODO
class BufferFooter(urwid.WidgetWrap):
    pass


class TimelineBuffer(urwid.WidgetWrap):
    """A widget that displays a `Timeline` object."""

    def __init__(self, timeline=[]):
        urwid.WidgetWrap.__init__(self, TimelineWidget(timeline))

    def clear(self):
        """Clears the buffer."""
        return self.render_timeline([])

    def render_timeline(self, timeline):
        """Renders the given statuses."""
        self._w = TimelineWidget(timeline)


class TimelineWidget(urwid.ListBox):
    """
    A `urwid.ListBox` containing a list of Twitter statuses, each of which is
    rendered as a `StatusWidget`.
    """

    def __init__(self, timeline):
        status_widgets = [StatusWidget(status) for status in timeline]
        urwid.ListBox.__init__(self, urwid.SimpleListWalker(status_widgets))


class StatusWidget(urwid.WidgetWrap):
    """Widget containing a Twitter status."""

    def __init__ (self, status):
        self.status = status
        self.id = status.id
        status_content = urwid.Padding(
            urwid.AttrWrap(urwid.Text(status.text), 'body'), left=1, right=1)
        # TODO!Header
        widget = urwid.AttrWrap(BoxDecoration(status_content, title=status.user.screen_name), 
                                              'line', 
                                              'focus')
        self.__super.__init__(widget)

    def selectable(self):
        return True

    def keypress(self, size, key):
        #TODO! modify widget attributes in response to certain actions
        return key


class BoxDecoration(urwid.WidgetDecoration, urwid.WidgetWrap):
    """Draw a box around `original_widget`."""

    def __init__(self, original_widget, title=''):
        self.color = 'header'
        if int(urwid.__version__[0]) == 1:
            urwid.utf8decode = lambda string: string

        def use_attr(a, t):
            if a:
                t = urwid.AttrWrap(t, a)
            return t

        # top line
        tline = None
        tline_attr = urwid.Columns([('fixed', 2, 
                                        urwid.Divider(urwid.utf8decode("─"))),
                                    ('fixed', len(title), 
                                        urwid.AttrWrap(urwid.Text(title), self.color)),
                                    urwid.Divider(urwid.utf8decode("─")),])
        tline = use_attr(tline, tline_attr)
        # bottom line
        bline = None
        bline = use_attr(bline, urwid.Divider(urwid.utf8decode("─")))
        # left line
        lline = None
        lline = use_attr(lline, urwid.SolidFill(urwid.utf8decode("│")))
        # right line
        rline = None
        rline = use_attr(rline, urwid.SolidFill(urwid.utf8decode("│")))
        # top left corner
        tlcorner = None
        tlcorner = use_attr(tlcorner, urwid.Text(urwid.utf8decode("┌")))
        # top right corner
        trcorner = None
        trcorner = use_attr(trcorner, urwid.Text(urwid.utf8decode("┐")))
        # bottom left corner
        blcorner = None
        blcorner = use_attr(blcorner, urwid.Text(urwid.utf8decode("└")))
        # bottom right corner
        brcorner = None
        brcorner = use_attr(brcorner, urwid.Text(urwid.utf8decode("┘")))

        # top
        top = urwid.Columns([('fixed', 1, tlcorner),
                             tline, 
                             ('fixed', 1, trcorner),])
        # middle
        middle = urwid.Columns([('fixed', 1, lline),
                                original_widget, 
                                ('fixed', 1, rline)], 
                               box_columns = [0,2], 
                               focus_column = 1)
        # bottom
        bottom = urwid.Columns([('fixed', 1, blcorner),
                                bline, 
                                ('fixed', 1, brcorner)])

        # widget decoration
        pile = urwid.Pile([('flow',top),
                           middle,
                           ('flow',bottom)], 
                          focus_item = 1)

        urwid.WidgetDecoration.__init__(self, original_widget)
        urwid.WidgetWrap.__init__(self, pile)
