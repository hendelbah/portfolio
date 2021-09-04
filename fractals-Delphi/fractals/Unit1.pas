unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, ExtCtrls, math, Menus, Buttons, GifImage, FTGifAnimate,
  XPMan;

type
  TForm1 = class(TForm)
    Edit1: TEdit;
    Edit2: TEdit;
    Edit3: TEdit;
    Button1: TSpeedButton;
    CheckBox2: TCheckBox;
    ComboBox1: TComboBox;
    Timer2: TTimer;
    Button2: TSpeedButton;
    Button3: TSpeedButton;
    Edit4: TEdit;
    Edit5: TEdit;
    Button4: TSpeedButton;
    Image1: TImage;
    Image2: TImage;
    Timer1: TTimer;
    Shape1: TShape;
    Timer3: TTimer;
    Label1: TLabel;
    SpeedButton1: TSpeedButton;
    XPManifest1: TXPManifest;
    Edit6: TEdit;
    SpeedButton2: TSpeedButton;
    procedure FormCreate(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure Edit2Change(Sender: TObject);
    procedure Edit3Change(Sender: TObject);
    procedure ComboBox1Change(Sender: TObject);
    procedure FormMouseWheelUp(Sender: TObject; Shift: TShiftState;
      MousePos: TPoint; var Handled: Boolean);
    procedure Timer2Timer(Sender: TObject);
    procedure FormMouseWheelDown(Sender: TObject; Shift: TShiftState;
      MousePos: TPoint; var Handled: Boolean);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Edit4Change(Sender: TObject);
    procedure Edit5Change(Sender: TObject);
    procedure Button4Click(Sender: TObject);
    procedure FormKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure FormKeyUp(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Image1Click(Sender: TObject);
    procedure FormMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormResize(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure Image2Click(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Timer3Timer(Sender: TObject);
    procedure SpeedButton1Click(Sender: TObject);
    procedure SpeedButton2Click(Sender: TObject);

  private
    { Private declarations }
  public
    { Public declarations }
  end;
/////////////////////////////////
  DrawThread = class(TThread)
  public
    procedure Execute; Override;
    procedure VCLOnEnd;
  end;
//
  SaveGif = class(TThread)
  public
    procedure Execute; Override;
  end;
/////////////////////////////////
const
sz=120;
rbr=50;  ro=240;  rp=60;  rs=120;
gbr=50;  go=120;  gp=60;  gs=120;
bbr=50;  bo=0;  bp=60;  bs=120;

xscale=3.5;
yscale=2.5;
ss=1.1;
maxpix=2048;
//
debug=false;
//
type
pRGBArray = ^TRGBArray;
TRGBArray = array[0..maxpix-1] of TRGBTriple;
TArrayOfBMP = array of TBitmap;
var
  Form1: TForm1;
  iter,h,w,a,mode,ii,giflength,step:integer;
  cx,cy,cx0,cy0,cx1,cy1,cxs,cys,scale,scale0,scale1,tt,x0g,y0g:extended;
  pal:array[1..(sz)] of TRGBTriple;
  black,red:TRGBTriple;
  p,cl:tpoint;
  m,mk,res,zoom,thread,clos,sav,savim:bool;
  rad:array[2..10] of extended;
  BitmapBufer,BitmapBufer1,imgb:tbitmap;
  bitmap1,bitmap2:pBitmap;
  gif:TArrayOfBMP;
  giff:TGifImage;
  dir:string;
implementation

{$R *.dfm}

procedure pallet1();
var
i,r,g,b,ri,gi,bi:integer;
begin
for I := 1 to sz do
begin
//red
  if ro/360<=1/2 then
    if i>(ro/360+1/2)*sz then  ri:=round((1+ro/360)*sz-i+1)
    else
      if i>ro/360*sz then  ri:=round(i-ro/360*sz)
      else  ri:=round(ro/360*sz-i+1)
  else
    if i<=(ro/360-1/2)*sz then  ri:=round((1-ro/360)*sz+i)
    else
      if i<=ro/360*sz then  ri:=round(ro/360*sz-i+1)
      else  ri:=round(i-ro/360*sz);

  if ri<=rs/360*sz then
    if ri>rp/360*sz then  r:=round((cos((ri-sz*rp/360)/(sz*(rs-rp)/360)*pi/2))*(255-rbr)+rbr)
    else  r:=255
  else r:=rbr;

//green
  if go/360<=1/2 then
    if i>(go/360+1/2)*sz then  gi:=round((1+go/360)*sz-i+1)
    else
      if i>go/360*sz then  gi:=round(i-go/360*sz)
      else  gi:=round(go/360*sz-i+1)
  else
    if i<=(go/360-1/2)*sz then  gi:=round((1-go/360)*sz+i)
    else
      if i<=go/360*sz then  gi:=round(go/360*sz-i+1)
      else  gi:=round(i-go/360*sz);

  if gi<=gs/360*sz then
    if gi>gp/360*sz then  g:=round((cos((gi-sz*gp/360)/(sz*(gs-gp)/360)*pi/2))*(255-gbr)+gbr)
    else  g:=255
  else g:=gbr;

//blue
  if bo/360<=1/2 then
    if i>(bo/360+1/2)*sz then  bi:=round((1+bo/360)*sz-i+1)
    else
      if i>bo/360*sz then  bi:=round(i-bo/360*sz)
      else  bi:=round(bo/360*sz-i+1)
  else
    if i<=(bo/360-1/2)*sz then  bi:=round((1-bo/360)*sz+i)
    else
      if i<=bo/360*sz then  bi:=round(bo/360*sz-i+1)
      else  bi:=round(i-bo/360*sz);

  if bi<=bs/360*sz then
    if bi>bp/360*sz then  b:=round((cos((bi-sz*bp/360)/(sz*(bs-bp)/360)*pi/2))*(255-bbr)+bbr)
    else  b:=255
  else b:=bbr;
  pal[i].rgbtRed:=r;
  pal[i].rgbtGreen:=g;
  pal[i].rgbtBlue:=b;
end;
end;

procedure SaveGif.Execute;
var
i,rslt,f:integer;
Ext:TGIFGraphicControlExtension;
LoopExt:TGIFAppExtNSLoop;
ex:bool;
image:  TGIFImage;
begin
giff:=TGifImage.Create;
f:=-1;
ex:=true;
while ex do
try
  f:=f+1;
  giff.LoadFromFile(dir+'\Fractal'+inttostr(f)+'.gif');
except
  on EFOpenError do ex:=false;
  else
end;
giff.Free;
giff:=TGifImage.Create;
giff.DitherMode:=dmnearest;
giff.Animate:=true;
giff.AnimationSpeed:=form1.Timer1.Interval;
//
image:= TGIFImage.Create();
image.Assign(gif[0]);
rslt:=giff.Add(image);
LoopExt := TGIFAppExtNSLoop.Create(giff.Images[Rslt]);
LoopExt.Loops := 0;
giff.Images[Rslt].Extensions.Add(LoopExt);
for I := 1 to length(gif) - 1 do
begin
  image.Assign(gif[i]);
  rslt:=giff.Add(image);
  Ext := TGIFGraphicControlExtension.Create(giff.Images[Rslt]);
  Ext.Delay := form1.Timer1.Interval div 10;
  giff.Images[Rslt].Extensions.Add(Ext);
end;

giff.OptimizeColorMap;
giff.SaveToFile(dir+'\Fractal'+inttostr(f)+'.gif');
f:=f+1;
giff.Free;
end;

procedure canresise(cr:bool);
begin
if cr then
begin
  form1.Constraints.MaxHeight:=form1.Height-form1.ClientHeight+650;
  form1.Constraints.MaxWidth:=form1.Width-form1.ClientWidth+1300;
  form1.Constraints.MinHeight:=0;
  form1.Constraints.MinWidth:=0;
end  else
begin
  form1.Constraints.MaxHeight:=form1.Height;
  form1.Constraints.MaxWidth:=form1.Width;
  form1.Constraints.MinHeight:=form1.Height;
  form1.Constraints.MinWidth:=form1.Width;
end;
end;

procedure paint1(row:pRGBArray;i:integer;col:TRGBTriple);
begin
row[i].rgbtRed:=col.rgbtRed;
row[i].rgbtGreen:=col.rgbtGreen;
row[i].rgbtBlue:=col.rgbtBlue;
end;

function calc(x,y,x0,y0:extended):integer;
var i,n,l:integer;
x1,y1:extended;
begin
x1:=0;
y1:=0;
n:=0;
l:=sqr(a);
for I := 1 to iter do
begin
  case a of
  2:
  begin
    x1:=sqr(x)-sqr(y)+x0;
    y1:=2*x*y+y0;
  end;
  3:
  begin
    x1:=power(x,3)-3*x*sqr(y)+x0;
    y1:=3*sqr(x)*y-power(y,3)+y0;
  end;
  4:
  begin
    x1:=power(x,4)+power(y,4)-6*sqr(x)*sqr(y)+x0;
    y1:=4*x*y*(sqr(x)-sqr(y))+y0;
  end;
  5:
  begin
    x1:=power(x,5)+5*x*power(y,4)-10*power(x,3)*sqr(y)+x0;
    y1:=y*(5*power(x,4)-10*sqr(x*y)+power(y,4))+y0;
  end;
  6:
  begin
    x1:=power(x,6)-15*power(x,4)*sqr(y)+15*sqr(x)*power(y,4)-power(y,6)+x0;
    y1:=6*power(x,5)*y-20*power(x,3)*power(y,3)+6*x*power(y,5)+y0;
  end;
  end;
  x:=x1;
  y:=y1;
  n:=i;
  if sqr(x1)+sqr(y1)>l then  break;
end;
result:=n;
end;

procedure Draw;

begin
  form1.Shape1.Brush.Color:=clyellow;
  form1.Shape1.Update;
  form1.Label1.Font.Color:=clblack;
  form1.Label1.Caption:='0';
  form1.Timer3.Tag:=0;
  form1.Timer3.Enabled:=true;
//
  a:=strtoint(form1.ComboBox1.Text);
  if not(form1.CheckBox2.Checked) and (a=2) then   cxs:=2/3 else  cxs:=1/2;
  if scale=1 then
  begin
    cx:=w*cxs;
    cy:=h*cys;
  end;
  cx1:=w*cxs;
  cy1:=h*cys;
  scale1:=1;
  cx0:=cx;
  cy0:=cy;
  scale0:=scale;
  if form1.CheckBox2.Checked then  mode:=3
  else
    if a=2 then  mode:=1  else  mode:=2;
  if form1.edit1.Text='' then form1.edit1.Text:=inttostr(iter);
  iter:=strtoint(form1.edit1.Text);
  x0g:=strtofloat(form1.Edit2.Text);
  y0g:=strtofloat(form1.Edit3.Text);
  form1.Button1.Enabled:=false;
  form1.Button2.Enabled:=false;
  canresise(false);
//
  thread:=true;
  DrawThread.Create(false);
//
end;

procedure DrawThread.Execute;
var
i,j,n,col:integer;
x,y,r,t,r0:extended;
row,row1:pRGBArray;
begin
try
  tbitmap(bitmap1).Width:=w;
  tbitmap(bitmap1).Height:=h;
  tbitmap(bitmap2).Width:=w;
  tbitmap(bitmap2).Height:=h;
  case mode of
  1:for j := 0 to h-1 do
    begin
      row:=pRGBArray(tbitmap(bitmap1).ScanLine[j]);
      for i := 0 to w-1 do
      begin
        x:=(i-cx)/w*xscale/scale;
        y:=(j-cy)/h*yscale/scale;
        r:=sqrt(sqr(x-1/4)+sqr(y));
        if x-1/4>0 then
          if y>=0 then  t:=arctan(y/(x-1/4))  else  t:=2*pi+arctan(y/(x-1/4))
        else
          if x-1/4=0 then t:=pi/2 else t:=pi+arctan(y/(x-1/4));
        if ((1/2-1/2*cos(t))>r) or (sqr(x+1)+sqr(y)<1/16)  then
          if debug then  paint1(row,i,red)  else  paint1(row,i,black)
        else
        begin
          n:=calc(0,0,x,y);
          col:=n mod sz+1;
          if n=iter then  paint1(row,i,black)
          else  paint1(row,i,pal[col]);
        end;
      end;
    end;
  2:for j := 0 to h-1 do
    begin
      row:=pRGBArray(tbitmap(bitmap1).ScanLine[j]);
      for i := 0 to w-1 do
      begin
        x:=(i-cx)/w*xscale/scale;
        y:=(j-cy)/h*yscale/scale;
        r:=sqrt(sqr(x)+sqr(y));
        r0:=rad[a]/(a-1);
        if x>0 then
          if y>=0 then  t:=arctan(y/x)  else  t:=2*pi+arctan(y/x)
        else
          if x=0 then t:=pi/2 else t:=pi+arctan(y/(x));
        if  sqr(r0)*(sqr(a)-2*a*(-abs(cos((t*(a-1)+pi)/2))*2+1)+1)>sqr(r)  then
          if debug then  paint1(row,i,red)  else  paint1(row,i,black)
        else
        begin
          n:=calc(0,0,x,y);
          col:=n mod sz+1;
          if n=iter then  paint1(row,i,black)
          else  paint1(row,i,pal[col]);
        end;
      end;
    end;
  3:for j := 0 to h-1 do
    begin
      row:=pRGBArray(tbitmap(bitmap1).ScanLine[j]);
      row1:=pRGBArray(tbitmap(bitmap2).ScanLine[h-1-j]);
      for i := 0 to w-1 do
      begin
        x:=(i-cx)/w*xscale/scale;
        y:=(j-cy)/h*yscale/scale;
        n:=calc(x,y,x0g,y0g);
        col:=n mod sz+1;
        if n=iter then
        begin
          paint1(row,i,black);
          paint1(row1,i,black);
        end  else
        begin
          paint1(row,i,pal[col]);
          paint1(row1,i,pal[col]);
        end;
      end;
    end;
  end;
  synchronize(VCLOnEnd);
finally
thread:=false;
end;
end;

procedure DrawThread.VCLOnEnd;
begin
  form1.Image1.Picture:=nil;
  form1.Image1.Stretch:=false;
  form1.Image1.Height:=h;
  form1.Image1.Width:=w;
  form1.Image1.Top:=0;
  form1.Image1.Left:=0;
  form1.Image1.Picture.Graphic:=tbitmap(bitmap1);
  if not form1.Timer1.Enabled then
  begin
    form1.Button1.Enabled:=true;
    form1.Button2.Enabled:=true;
    canresise(true);
  end;
  form1.Shape1.Brush.Color:=cllime;
  form1.Shape1.Update;
  form1.Timer3.Enabled:=false;
if debug then
begin
  form1.Image1.Canvas.pen.Color:=clred;
  form1.Image1.Canvas.MoveTo(round(cx),0);
  form1.Image1.Canvas.LineTo(round(cx),h);
  form1.Image1.Canvas.MoveTo(0,round(cy));
  form1.Image1.Canvas.LineTo(w,round(cy));
end;
end;

procedure reset();
begin
  if not(form1.CheckBox2.Checked) and (a=2) then   cxs:=2/3 else  cxs:=1/2;
  scale:=1;
  cx1:=cx;
  cy1:=cy;
  scale1:=scale;
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
bitmap1:=pbitmap(BitmapBufer);
draw;
end;

procedure TForm1.Button2Click(Sender: TObject);
begin
res:=false;
form1.ClientWidth:=round(form1.ClientHeight/yscale*xscale);
reset;
bitmap1:=pbitmap(BitmapBufer);
draw;
end;

procedure TForm1.Button3Click(Sender: TObject);
var
r,t,x0,y0:extended;
begin
x0:=strtofloat(edit2.Text);
y0:=strtofloat(edit3.Text);
r:=sqrt(sqr(x0)+sqr(y0));
if x0>0 then
  if y0>=0 then  t:=arctan(y0/x0)  else  t:=2*pi+arctan(y0/x0)
else
  if x0=0 then t:=pi/2 else t:=pi+arctan(y0/(x0));

Edit4.Text:=floattostr(simpleroundto(r,-10));
Edit5.Text:=floattostr(simpleroundto(t/pi*180,-10));
end;

procedure TForm1.Button4Click(Sender: TObject);
begin
Edit2.Text:=floattostr(simpleroundto(strtofloat(edit4.Text)*cos(strtofloat(edit5.Text)/180*pi),-10));
Edit3.Text:=floattostr(simpleroundto(strtofloat(edit4.Text)*sin(strtofloat(edit5.Text)/180*pi),-10));
end;

procedure TForm1.ComboBox1Change(Sender: TObject);
begin
if form1.ComboBox1.ItemIndex=-1 then form1.ComboBox1.ItemIndex:=0;
reset;
form1.ActiveControl:=nil;
form1.SetFocus;
end;

procedure TForm1.Edit2Change(Sender: TObject);
var
d:boolean;
i:integer;
s:string;
begin

s:=edit2.text;
if (length(s)>0) then
begin
  if not((s[length(s)]='0') or (s[length(s)]='1') or (s[length(s)]='2') or (s[length(s)]='3') or (s[length(s)]='4') or (s[length(s)]='5') or (s[length(s)]='6') or (s[length(s)]='7') or (s[length(s)]='8') or (s[length(s)]='9')) then
  case s[length(S)] of
    '.':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) or (s='-') then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end;
    '-':    if length(S)>1 then  delete(s,length(s),1);
    ',':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) or (s='-') then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end
    else  delete(s,length(s),1);
  end;
  if not(edit2.text=s) then
  begin
    edit2.text:=s;
    edit2.SelStart:=length(S)+1;
  end;
end;

end;

procedure TForm1.Edit3Change(Sender: TObject);
var
d:boolean;
i:integer;
s:string;
begin
s:=edit3.text;
if (length(s)>0) then
begin
  if not((s[length(s)]='0') or (s[length(s)]='1') or (s[length(s)]='2') or (s[length(s)]='3') or (s[length(s)]='4') or (s[length(s)]='5') or (s[length(s)]='6') or (s[length(s)]='7') or (s[length(s)]='8') or (s[length(s)]='9')) then
  case s[length(S)] of
    '.':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) or (s='-') then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end;
    '-':    if length(S)>1 then  delete(s,length(s),1);
    ',':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) or (s='-') then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end
    else  delete(s,length(s),1);
  end;
  if not(edit3.text=s) then
  begin
    edit3.text:=s;
    edit3.SelStart:=length(S)+1;
  end;
end;

end;

procedure TForm1.Edit4Change(Sender: TObject);
var
d:boolean;
i:integer;
s:string;
begin
s:=edit4.text;
if (length(s)>0) then
begin
  if not((s[length(s)]='0') or (s[length(s)]='1') or (s[length(s)]='2') or (s[length(s)]='3') or (s[length(s)]='4') or (s[length(s)]='5') or (s[length(s)]='6') or (s[length(s)]='7') or (s[length(s)]='8') or (s[length(s)]='9')) then
  case s[length(S)] of
    '.':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end;
    ',':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end
    else  delete(s,length(s),1);
  end;
  if not(edit4.text=s) then
  begin
    edit4.text:=s;
    edit4.SelStart:=length(S)+1;
  end;
end;

end;

procedure TForm1.Edit5Change(Sender: TObject);
var
d:boolean;
i:integer;
s:string;
begin

s:=edit5.text;
if (length(s)>0) then
begin
  if not((s[length(s)]='0') or (s[length(s)]='1') or (s[length(s)]='2') or (s[length(s)]='3') or (s[length(s)]='4') or (s[length(s)]='5') or (s[length(s)]='6') or (s[length(s)]='7') or (s[length(s)]='8') or (s[length(s)]='9')) then
  case s[length(S)] of
    '.':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) or (s='-') then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end;
    '-':    if length(S)>1 then  delete(s,length(s),1);
    ',':
    begin
      delete(s,length(s),1);
      d:=true;
      if (length(s)=0) or (s='-') then  s:=s+'0,' else
      for i := 1 to length(s) do
      if s[i]=',' then  d:=false;
      if d then  s:=s+',';
    end
    else  delete(s,length(s),1);
  end;
  if not(edit5.text=s) then
  begin
    edit5.text:=s;
    edit5.SelStart:=length(S)+1;
  end;
end;

end;

procedure TForm1.FormClose(Sender: TObject; var Action: TCloseAction);
begin

if thread then
begin
  action:=canone;
  form1.Timer1.Enabled:=true;
  clos:=true;
end;
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
m:=false;  mk:=false;  res:=true;  zoom:=true;  thread:=false;  clos:=false;  sav:=false;  savim:=false;
BitmapBufer:=tbitmap.Create;
BitmapBufer.PixelFormat:=pf24bit;
BitmapBufer1:=tbitmap.Create;
BitmapBufer1.PixelFormat:=pf24bit;
bitmap2:=pbitmap(BitmapBufer1);
imgb:=tbitmap.Create;
imgb.PixelFormat:=pf24bit;
image1.Top:=0;
image1.Left:=0;
//
if form1.ComboBox1.ItemIndex=-1 then form1.ComboBox1.ItemIndex:=0;
a:=strtoint(form1.ComboBox1.Text);
iter:=strtoint(edit1.Text);
h:=form1.ClientHeight;
w:=round(h/yscale*xscale);
if not(form1.CheckBox2.Checked) and (a=2) then   cxs:=2/3 else  cxs:=1/2;
cys:=1/2;
cx:=w*cxs;  cx0:=cx;
cy:=h*cys;  cy0:=cy;
scale:=1;   scale0:=scale;
cx1:=w*cxs;
cy1:=h*cys;
scale1:=1;
//
res:=false;
form1.ClientWidth:=round(form1.ClientHeight/yscale*xscale);
res:=false;
//
form1.Constraints.MaxHeight:=form1.Height-form1.ClientHeight+650;
form1.Constraints.MaxWidth:=form1.Width-form1.ClientWidth+1300;
//
pallet1;
rad[2]:=0.25;
rad[3]:=0.3845;
rad[4]:=0.472;
rad[5]:=0.5345;
rad[6]:=0.582;
black.rgbtRed:=0;
black.rgbtGreen:=0;
black.rgbtBlue:=0;
red.rgbtRed:=150;
red.rgbtGreen:=0;
red.rgbtBlue:=0;
dir:=getcurrentdir;
//

end;




procedure TForm1.FormDestroy(Sender: TObject);
begin
BitmapBufer.Free;
BitmapBufer1.Free;
imgb.Free;
end;

procedure TForm1.FormKeyDown(Sender: TObject; var Key: Word;
  Shift: TShiftState);
begin
if not thread then
begin
  if key=13 then
  begin
    bitmap1:=pbitmap(BitmapBufer);
    draw;
  end;
  if (Key=17) and not(timer2.Enabled) and not(thread) then
  begin
    mk:=true;
    form1.ActiveControl:=nil;
    form1.SetFocus;
  end;
end;
end;

procedure TForm1.FormKeyUp(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
if Key=17 then  mk:=false;
end;

procedure TForm1.FormMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
case button of
  mbright:
  begin
    form1.Edit2.Text:=floattostr(simpleroundto((X-cx)/w*xscale/scale,-12));
    form1.Edit3.Text:=floattostr(simpleroundto((Y-cy)/h*yscale/scale,-12));
  end;
  mbleft: if mk then
  begin
    m:=true;
    getcursorpos(cl);
    cl.X:=cl.X-form1.ClientOrigin.X;
    cl.Y:=cl.Y-form1.ClientOrigin.y;
  end;
end;

end;

procedure TForm1.FormMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
var cl1:tpoint;
begin
if m then
begin
  getcursorpos(cl1);
  cl1.X:=cl1.X-form1.ClientOrigin.X;
  cl1.Y:=cl1.Y-form1.ClientOrigin.Y;
  cx:=cx+cl1.X-cl.X;
  cy:=cy+cl1.Y-cl.Y;
  bitmap1:=pbitmap(BitmapBufer);
  draw;
end;
m:=false;
end;

procedure TForm1.FormMouseWheelDown(Sender: TObject; Shift: TShiftState;
  MousePos: TPoint; var Handled: Boolean);
begin
if zoom and not(thread) then
begin
  getcursorpos(p);
  p.X:=p.X-form1.ClientOrigin.X;
  p.y:=p.y-form1.ClientOrigin.y;
  if scale/ss>1 then
  begin
    cx:=p.X+(cx-p.x)/ss ;
    cy:=p.y+(cy-p.y)/ss ;
    scale:=scale/ss;
//
    cx1:=p.X+(cx1-p.x)/ss ;
    cy1:=p.y+(cy1-p.y)/ss ;
    scale1:=scale1/ss;
//
    form1.Image1.Stretch:=true;
    form1.Image1.Left:=round(cx1-w*cxs*scale1);
    form1.Image1.Top:=round(cy1-h*cys*scale1);
    form1.Image1.Width:=round(w*scale1);
    form1.Image1.Height:=round(h*scale1);
//
    canresise(false);
    timer2.Enabled:=true;
    timer2.Tag:=0;
  end
  else
  begin
    form1.Image1.Left:=round(w*cxs-cx0/scale0);
    form1.Image1.Top:=round(h*cys-cy0/scale0);
    form1.Image1.Width:=round(w/scale0);
    form1.Image1.Height:=round(h/scale0);
    form1.Image1.Update;
    reset;
    timer2.Enabled:=false;
    if scale0<>1 then
    begin
      bitmap1:=pbitmap(BitmapBufer);
      draw;
    end;
  end;
end;

end;

procedure TForm1.FormMouseWheelUp(Sender: TObject; Shift: TShiftState;
  MousePos: TPoint; var Handled: Boolean);

begin
if zoom and not(thread) then
begin
  getcursorpos(p);
  p.X:=p.X-form1.ClientOrigin.X;
  p.y:=p.y-form1.ClientOrigin.y;
//
  cx:=p.X+(cx-p.x)*ss ;
  cy:=p.y+(cy-p.y)*ss ;
  scale:=scale*ss;
  cx1:=p.X+(cx1-p.x)*ss ;
  cy1:=p.y+(cy1-p.y)*ss ;
  scale1:=scale1*ss;
//
  form1.Image1.Stretch:=true;
  form1.Image1.Left:=round(cx1-w*cxs*scale1);
  form1.Image1.Top:=round(cy1-h*cys*scale1);
  form1.Image1.Width:=round(w*scale1);
  form1.Image1.Height:=round(h*scale1);
//
  canresise(false);
  timer2.Enabled:=true;
  timer2.Tag:=0;
  end;
end;

procedure TForm1.FormResize(Sender: TObject);
begin
h:=form1.ClientHeight;
w:=form1.ClientWidth;
form1.Image1.Stretch:=true;
form1.Image1.Height:=h;
form1.Image1.Width:=w;
cx:=cx0*w/(cx1/cxs);
cy:=cy0*h/(cy1/cys);
if res then
begin
  zoom:=false;
  timer2.Enabled:=true;
  timer2.Tag:=0;
end;
res:=true;
end;

procedure TForm1.FormShow(Sender: TObject);
var
i,j:integer;
r:extended;
row:pRGBArray;
begin
BitmapBufer.Width:=w;
BitmapBufer.Height:=h;
for j := 0 to h-1 do
begin
  row:=pRGBArray(BitmapBufer.ScanLine[j]);
  for i := 0 to w-1 do
  begin
    r:=sqrt(sqr(i-w/2)+sqr(j-h/2));
    paint1(row,i,pal[round(r)mod sz+1]);
  end;
end;
form1.Image1.Picture.Graphic:=BitmapBufer;
imgb.Width:=form1.Image2.Width;
imgb.Height:=form1.Image2.Height;
for j := 0 to form1.Image2.Height - 1 do
begin
  row:=pRGBArray(imgb.ScanLine[j]);
  for I := 0 to form1.Image2.Width - 1 do
    paint1(row,i,pal[round((i+1)/form1.Image2.Width*sz)]);
end;
form1.Image2.Picture.Graphic:=imgb;
form1.ActiveControl:=nil;
form1.SetFocus;
end;

procedure TForm1.Image1Click(Sender: TObject);
begin
form1.ActiveControl:=nil;
form1.SetFocus;
end;

procedure TForm1.Image2Click(Sender: TObject);
var i:integer;
begin
form1.ActiveControl:=nil;
form1.SetFocus;
form1.Timer1.Enabled:=not(form1.Timer1.Enabled);
if form1.Timer1.Enabled then
begin
  step:=strtoint(form1.Edit6.Text);
  if a<>strtoint(form1.ComboBox1.Text) then
  begin
    sav:=false;
    for I := 0 to giflength do
    gif[i].Free;
    a:=strtoint(form1.ComboBox1.Text);
    tt:=-step/4/(a-1);
  end  else
  a:=strtoint(form1.ComboBox1.Text);
  form1.CheckBox2.Checked:=true;
  form1.CheckBox2.Enabled:=false;
  form1.Button1.Enabled:=false;
  form1.Button2.Enabled:=false;
  form1.Button3.Enabled:=false;
  form1.Button4.Enabled:=false;
  form1.Edit1.Enabled:=false;
  form1.Edit2.Enabled:=false;
  form1.Edit3.Enabled:=false;
  form1.ComboBox1.Enabled:=false;
  canresise(false);
  giflength:=(1440*(a-1)) div step;
  if not sav then  setlength(gif,giflength);
end
else
begin
  if not thread then
  begin
    form1.Button1.Enabled:=true;
    form1.Button2.Enabled:=true;
    canresise(true);
  end;
  form1.CheckBox2.Enabled:=true;
  form1.Button3.Enabled:=true;
  form1.Button4.Enabled:=true;
  form1.Edit1.Enabled:=true;
  form1.Edit2.Enabled:=true;
  form1.Edit3.Enabled:=true;
  form1.ComboBox1.Enabled:=true;
end;
end;

procedure TForm1.SpeedButton1Click(Sender: TObject);
var ex:bool;
f:integer;
begin
f:=-1;
ex:=true;
while ex do
try
  f:=f+1;
  BitmapBufer.LoadFromFile(dir+'\Fractal'+inttostr(f)+'.bmp');
except
  on EFOpenError do ex:=false;
  else
end;
form1.Image1.Picture.Bitmap.SaveToFile(dir+'\Fractal'+inttostr(f)+'.bmp');
end;

procedure TForm1.SpeedButton2Click(Sender: TObject);
begin
savegif.Create(false);
end;

procedure TForm1.Timer1Timer(Sender: TObject);
var
i,j,sp:integer;
row:pRGBArray;
r:extended;
begin
sp:=1;
imgb.Width:=form1.Image2.Width;
imgb.Height:=form1.Image2.Height;
for j := 0 to form1.Image2.Height - 1 do
begin
  row:=pRGBArray(imgb.ScanLine[j]);
  for I := 0 to form1.Image2.Width - 1 do
    paint1(row,i,pal[round(((i+timer1.Tag*sp) mod form1.Image2.Width+1)/form1.Image2.Width*sz)]);
end;
form1.Image2.Picture.Graphic:=imgb;
/////////////////////////////////////
if not(thread) then
if clos then  form1.Close  else
begin
  tt:=tt+step/4/(a-1);
  if tt>=360 then  tt:=0;
  r:=rad[a]/(a-1)*sqrt(sqr(a)-2*a*((cos((tt/180*pi)*(a-1))-1)/2*(1+(sqr(1-0.01*(15-a))/(2*a*sqr(rad[a]/(a-1)))-a/2-1/2/a))+1)+1)+0.01*(15-a);
  edit5.Text:=floattostr(simpleroundto(tt,-6));
  edit4.Text:=floattostr(simpleroundto(r,-10));
  if a=2 then  Edit2.Text:=floattostr(simpleroundto(r*cos(tt/180*pi)+0.25,-10))  else
  Edit2.Text:=floattostr(simpleroundto(r*cos(tt/180*pi),-10));
  Edit3.Text:=floattostr(simpleroundto(r*sin(tt/180*pi),-10));
  ii:=round(tt*(a-1)*4/step);
  if not sav then
  begin
    gif[ii]:=TBitmap.Create;
    gif[ii].PixelFormat:=pf24bit;
    bitmap1:=pbitmap(gif[ii]);
    if (ii=0)  then  bitmap2:=pbitmap(BitmapBufer1)  else
      if   ii>=giflength/2  then
      begin
        bitmap2:=pbitmap(BitmapBufer1);
        sav:=true;
//        savim:=true;
      end  else
        begin
          ii:=giflength-ii;
          gif[ii]:=TBitmap.Create;
          gif[ii].PixelFormat:=pf24bit;
          bitmap2:=pbitmap(gif[ii]);
        end;
    draw;
  end
  else  form1.Image1.Picture.Graphic:=gif[ii];
end;
if timer1.Tag<form1.Image2.Width/sp then  timer1.Tag:=timer1.Tag+1 else timer1.Tag:=1;
end;

procedure TForm1.Timer2Timer(Sender: TObject);
begin
timer2.Tag:=timer2.Tag+1;
if timer2.Tag=10 then
  begin
    zoom:=true;
    bitmap1:=pbitmap(BitmapBufer);
    draw;
    timer2.Enabled:=false;
  end;
end;

procedure TForm1.Timer3Timer(Sender: TObject);
begin
form1.Label1.Caption:=floattostr(form1.Timer3.Tag*form1.Timer3.Interval/1000)+'s';
form1.Timer3.Tag:=form1.Timer3.Tag+1;
end;

end.
