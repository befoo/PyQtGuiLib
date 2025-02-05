from PyQtGuiLib.header import (
    QWidget,
    QPainter,
    QPaintEvent,
    QPolygonF,
    QFont,
    QColor,
    QPointF,
    QBrush,
    textSize,
    QPainterPath,
    QRect,
    QPen,
    qt,
    pyqtProperty
)
from PyQtGuiLib.core.widgets import WidgetABC

class BubbleWidget(WidgetABC):

    # 方向
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(100,60)

        # self.setAttribute(qt.WA_StyledBackground, True)
        # self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)

        # 箭头高度(三角形)
        self._arrows_h = 16

        # 文字
        self.text = ""

        # 追踪的控件
        self.trackWidget = None #type:QWidget

        self.direction = BubbleWidget.Down

        #
        self.setText("气泡窗口")

    def set_Arrows(self,size:int):
        self._arrows_h = size

    def get_Arrows(self) -> int:
        return self._arrows_h
    # ----------------

    # 设置文字
    def setText(self,text:str):
        self.text = text
        self.textExtend()

    # 文字扩展
    def textExtend(self):
        f = QFont()
        f.setPointSize(self.get_fontSize())
        # 文字大小
        fs = textSize(f, self.text)
        fw = fs.width()
        fh = fs.height()

        if self.direction in [BubbleWidget.Top,BubbleWidget.Down]:
            self.resize(fw + 30, self.height())
        else:
            self.resize(fw + 30+self._arrows_h, self.height())

        if fh >= self.height():
            self.resize(self.width(),self.height()+40)

        self.setTrack(self.trackWidget)

    # 设置气泡箭头方向
    def setDirection(self,d):
        self.direction = d

    # 控件追踪
    def setTrack(self, widget: QWidget):
        if widget is None:
            return

        self.trackWidget = widget

        x,y = widget.x(),widget.y()
        w,h = widget.width(),widget.height()
        cx = widget.x()+w//2-self.width()//2  # x轴中心
        cy = widget.y()+h//2-self.height()//2

        if self.direction == BubbleWidget.Top:
            self.move(cx,y+h)
        elif self.direction == BubbleWidget.Left:
            self.move(x+w,cy)
        elif self.direction == BubbleWidget.Right:
            self.move(x-self.width(),cy)
        else:
            self.move(cx,y-self.height())

    # 绘制气泡
    def drawBubble(self,painter:QPainter,ppath:QPainterPath):
        # 矩形高度
        rect_h = self.height() - self._arrows_h
        rect_w = self.width() - self._arrows_h
        # 画三角
        line_w = self._arrows_h  # 线宽
        lien_x = self.width() // 2 - line_w // 2  # 线的位置-水平
        line_y = self.height()//2  # 线的位置-垂直

        # 绘制文字
        f = QFont()
        f.setPointSize(self.get_fontSize())
        painter.setFont(f)
        # 文字大小
        fs = textSize(f, self.text)
        fw = fs.width()
        fh = fs.height()

        self.textExtend()

        # 画刷
        bru = QBrush(self.get_backgroundColor())
        painter.setBrush(bru)

        # 画笔
        painter.setPen(qt.NoPen)

        if self.direction == BubbleWidget.Top:
            # 画三角
            ploys = [QPointF(lien_x,self._arrows_h,),QPointF(lien_x+line_w//2,1),
                     QPointF(lien_x+line_w,self._arrows_h)
                     ]
            # 画矩形
            rect = QRect(self.get_margin(),self._arrows_h+self.get_margin(),self.width()-self.get_margin()*2,rect_h-self.get_margin()*2)
            # 文字位置
            x = self.width() // 2 - fw // 2
            y = rect_h//2 + fh//2+self._arrows_h
        elif self.direction == BubbleWidget.Left:
            # 画三角
            ploys = [QPointF(1,line_y),QPointF(self._arrows_h,line_y-line_w//2),
                     QPointF(self._arrows_h,line_y+line_w//2)
            ]
            rect = QRect(self._arrows_h+self.get_margin(),self.get_margin(),rect_w-self.get_margin()*2,self.height()-self.get_margin()*2)
            # 文字位置
            x = self.width()//2-fw//2 + self._arrows_h//2
            y = self.height()//2 + fh//2
        elif self.direction == BubbleWidget.Right:
            # 画三角
            ploys =[QPointF(rect_w,line_y-line_w//2),QPointF(rect_w+self._arrows_h,line_y),
                    QPointF(rect_w,line_y+line_w//2)
            ]
            rect = QRect(self.get_margin(),self.get_margin(),rect_w-self.get_margin()*2,self.height()-self.get_margin()*2)
            # 文字位置
            x = (self.width()-self._arrows_h)//2 - fw//2
            y = self.height()//2 + fh//2
        else: # Down
            rect = QRect(self.get_margin(),self.get_margin(),self.width()-self.get_margin()*2,rect_h-self.get_margin()*2)
            # 画三角
            ploys =[QPointF(lien_x,rect_h),
                    QPointF(lien_x+line_w//2,rect_h+self._arrows_h),
                    QPointF(lien_x+line_w,rect_h)]
            # 文字位置
            x = self.width() // 2 - fw//2
            y = rect_h // 2 + fh//2
        # 绘制矩形
        painter.drawRoundedRect(rect, self.get_radius(), self.get_radius())
        # 绘制三角形
        ppath.addPolygon(QPolygonF(ploys))
        painter.fillPath(ppath, self.get_backgroundColor())
        # 绘制文字
        op = QPen()
        op.setColor(QColor(255, 255, 255))
        painter.setPen(op)
        painter.drawText(x,y, self.text)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        ppath = QPainterPath()

        # 绘制气泡
        self.drawBubble(painter,ppath)

        painter.end()

    # 专属QSS
    arrowsSize = pyqtProperty(int,fset=set_Arrows,fget=get_Arrows)
