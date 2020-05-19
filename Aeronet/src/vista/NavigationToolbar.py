'''
Created on 10 mar. 2020

Modificación de  matplotlib.backends.backend_qt5agg.NavigationToolbar2QT
'''

import os
import sys

import matplotlib

from weakref import WeakKeyDictionary
from matplotlib import cbook
from matplotlib.backend_bases import (
     NavigationToolbar2, cursors)
import matplotlib.backends.qt_editor.figureoptions as figureoptions

from PyQt5 import (
    QtCore, QtGui, QtWidgets)

cursord = {
    cursors.MOVE: QtCore.Qt.SizeAllCursor,
    cursors.HAND: QtCore.Qt.PointingHandCursor,
    cursors.POINTER: QtCore.Qt.ArrowCursor,
    cursors.SELECT_REGION: QtCore.Qt.CrossCursor,
    cursors.WAIT: QtCore.Qt.WaitCursor,
    }

class NavigationToolbar(NavigationToolbar2, QtWidgets.QToolBar):
    
    def __init__(self, canvas, parent, coordinates=True):
        """ coordinates: should we show the coordinates on the right? """
        self.canvas = canvas
        self.parent = parent
        self._nav_stack = cbook.Stack()
        self.coordinates = coordinates
        self._actions = {}
        """A mapping of toolitem method names to their QActions"""
        self.toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        #('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        # ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        # ('Save', 'Save the figure', 'filesave', 'save_figure'),
        )
        
        QtWidgets.QToolBar.__init__(self, parent)
        NavigationToolbar2.__init__(self, canvas)

    def _icon(self, name):
        
        name = name.replace('.png', '_large.png')
        pm = QtGui.QPixmap(os.path.join(self.basedir, name))
        if hasattr(pm, 'setDevicePixelRatio'):
            pm.setDevicePixelRatio(self.canvas._dpi_ratio)
        return QtGui.QIcon(pm)

    def _init_toolbar(self):
        self.basedir = os.path.join(matplotlib.rcParams['datapath'], 'images')

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.addSeparator()
            else:
                a = self.addAction(self._icon(image_file + '.png'),
                                   text, getattr(self, callback))
                self._actions[callback] = a
                if callback in ['zoom', 'pannn']:
                    a.setCheckable(True)
                if tooltip_text is not None:
                    a.setToolTip(tooltip_text)

        self.buttons = {}

        # Add the x,y location widget at the right side of the toolbar
        # The stretch factor is 1 which means any resizing of the toolbar
        # will resize this label instead of the buttons.
        if self.coordinates:
            self.locLabel = QtWidgets.QLabel("", self)
            self.locLabel.setAlignment(
                    QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self.locLabel.setSizePolicy(
                QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                      QtWidgets.QSizePolicy.Ignored))
            labelAction = self.addWidget(self.locLabel)
            labelAction.setVisible(True)

        # reference holder for subplots_adjust window
        self.adj_window = None

        # Esthetic adjustments - we need to set these explicitly in PyQt5
        # otherwise the layout looks different - but we don't want to set it if
        # not using HiDPI icons otherwise they look worse than before.
        
        self.setIconSize(QtCore.QSize(24, 24))
        self.layout().setSpacing(12)

    
        # For some reason, self.setMinimumHeight doesn't seem to carry over to
        # the actual sizeHint, so override it instead in order to make the
        # aesthetic adjustments noted above.
        def sizeHint(self):
            size = super().sizeHint()
            size.setHeight(max(48, size.height()))
            return size

    def edit_parameters(self):
        allaxes = self.canvas.figure.get_axes()
        if not allaxes:
            QtWidgets.QMessageBox.warning(
                self.parent, "Error", "There are no axes to edit.")
            return
        elif len(allaxes) == 1:
            axes, = allaxes
        else:
            titles = []
            for axes in allaxes:
                name = (axes.get_title() or
                        " - ".join(filter(None, [axes.get_xlabel(),
                                                 axes.get_ylabel()])) or
                        "<anonymous {} (id: {:#x})>".format(
                            type(axes).__name__, id(axes)))
                titles.append(name)
            item, ok = QtWidgets.QInputDialog.getItem(
                self.parent, 'Customize', 'Select axes:', titles, 0, False)
            if ok:
                axes = allaxes[titles.index(item)]
            else:
                return

        figureoptions.figure_edit(axes, self)
    
    #Activa el botón zoom
    def _update_buttons_checked(self):
        self._actions['zoom'].setChecked(self._active == 'ZOOM')

    def zoom(self, *args):
        super().zoom(*args)
        self._update_buttons_checked()

    def set_message(self, s):
        if self.coordinates:
            self.locLabel.setText(s)

    def set_cursor(self, cursor):
        self.canvas.setCursor(cursord[cursor])

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0
        rect = [int(val) for val in (x0, y0, x1 - x0, y1 - y0)]
        self.canvas.drawRectangle(rect)

    def remove_rubberband(self):
        self.canvas.drawRectangle(None)
    
    #Limpia el cursor sobre la grafica para sincronizar con el slider
    def clearCursor(self):
        self._nav_stack.clear()
    
    #Actualiza las coordenadas actuales de la gráfica    
    def push_current(self):
        """Push the current view limits and position onto the stack."""
        self._nav_stack.push(
            WeakKeyDictionary(
                {ax: (ax._get_view(),
                      # Store both the original and modified positions.
                      (ax.get_position(True).frozen(),
                       ax.get_position().frozen()))
                 for ax in self.canvas.figure.axes}))
        self.set_history_buttons()
