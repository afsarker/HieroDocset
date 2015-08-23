# Shows how to add custom columns to the Spreadsheet view
import hiero.ui
import PySide.QtCore
import PySide.QtGui

_itemData = dict() # Just for example purposes. In real life, you'd store this in the model

class CustomSpreadsheetColumns(object):
  """
    A class defining custom columns for Hiero's spreadsheet view. This has a similar, but
    slightly simplified, interface to the QAbstractItemModel and QItemDelegate classes.
  """

  def numColumns(self):
    """
      Return the number of custom columns in the spreadsheet view
    """
    return 3

  def columnName(self, column):
    """
      Return the name of a custom column
    """
    if column == 0:
      return "Python Tags"
    if column == 1:
      return "Python Name"
    if column == 2:
      return "Python Row"
    return ""

  def getData(self, row, column, item):
    """
      Return the data in a cell
    """
    if column == 0:
      return ""
    if column == 1:
      if item in _itemData:
        return str(_itemData[item])
      return item.name()
    if column == 2:
      return str(row+1)
    return None

  def setData(self, row, column, item, data):
    """
      Set the data in a cell
    """
    print "setData", (self, row, column, item, data)
    _itemData[item] = str(data)

  def getTooltip(self, row, column, item):
    """
      Return the tooltip for a cell
    """
    return "Tooltip: "+str(row)+"/"+str(column)+": "+item.name()

  def getFont(self, row, column, item):
    """
      Return the tooltip for a cell
    """
    if column == 1:
      return PySide.QtGui.QFont("Courier", 24)
    return None

  def getBackground(self, row, column, item):
    """
      Return the background colour for a cell
    """
    if column == 1:
      return PySide.QtGui.QColor(64, 255, 64)
    return None

  def getForeground(self, row, column, item):
    """
      Return the text colour for a cell
    """
    if column == 1:
      return PySide.QtGui.QColor(255, 64, 64)
    return None

  def getIcon(self, row, column, item):
    """
      Return the icon for a cell
    """
    if column == 1:
      return PySide.QtGui.QIcon("icons:Add.png")
    return None

  def getSizeHint(self, row, column, item):
    """
      Return the size hint for a cell
    """
    if column == 0:
      return PySide.QtCore.QSize(300, 32)
    return None

  def paintCell(self, row, column, item, painter, option):
    """
      Paint a custom cell. Return True if the cell was painted, or False to continue
      with the default cell painting.
    """
    if column == 0:
      if option.state & PySide.QtGui.QStyle.State_Selected:
        painter.fillRect(option.rect, option.palette.highlight())
      iconSize = 20
      r = PySide.QtCore.QRect(option.rect.x(), option.rect.y()+(option.rect.height()-iconSize)/2, iconSize, iconSize)
      tags = item.tags()
      if len(tags) > 0:
        painter.save()
        painter.setClipRect(option.rect)
        for tag in item.tags():
          PySide.QtGui.QIcon(tag.icon()).paint(painter, r, PySide.QtCore.Qt.AlignLeft)
          r.translate(r.width()+2, 0)
        painter.restore()
        return True
    return False

  def createEditor(self, row, column, item, view):
    """
      Create an editing widget for a custom cell
    """
    tags = item.tags()
    if len(tags) > 0:
      cb = PySide.QtGui.QComboBox()
      for tag in tags:
        cb.addItem(PySide.QtGui.QIcon(tag.icon()), tag.name())
      cb.currentIndexChanged.connect(self.indexChanged);
      print "createEditor:", (self, row, column, item, view)
      return cb
    return None

  def setEditorData(self, row, column, item, editor):
    """
      Update the custom editor from the model data. Return True if this was done.
    """
    print "setEditorData:", (self, row, column, item, editor)
    if column == 1:
      try:
        print " - setEditorData:", _itemData[item]
        index = int(_itemData[item])
        editor.setCurrentIndex(index)
      except:
        print "No existing data for item"
      return True
    return False

  def setModelData(self, row, column, item, editor):
    """
      Update the model data from the custom editor. Return True if this was done.
    """
    print "setModelData:", (self, row, column, item, editor)
    if column == 1:
      _itemData[item] = str(editor.currentIndex())
      print " - setModelData:", _itemData[item]
      return True
    return False

  def dropMimeData(self, row, column, item, data, items):
    """
      Handle a drag and drop operation
    """
    print "dropMimeData", (self, row, column, item, data.formats(), items)
    return None


  def indexChanged(self, index):
    """
      This method is called when our custom widget changes index.
    """
    print "ComboBox index changed:", index

# Register our custom columns
hiero.ui.customColumn = CustomSpreadsheetColumns()
