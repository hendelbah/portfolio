object Form1: TForm1
  Left = 0
  Top = 0
  Hint = 'Switch to Julia set, using source point specified in left fields'
  AlphaBlend = True
  Caption = #1060#1088#1072#1082#1090#1072#1083#1099
  ClientHeight = 350
  ClientWidth = 700
  Color = clBtnFace
  Constraints.MaxHeight = 650
  Constraints.MaxWidth = 1300
  DoubleBuffered = True
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  Position = poDesigned
  ShowHint = True
  OnClose = FormClose
  OnCreate = FormCreate
  OnDestroy = FormDestroy
  OnKeyDown = FormKeyDown
  OnKeyUp = FormKeyUp
  OnMouseDown = FormMouseDown
  OnMouseUp = FormMouseUp
  OnMouseWheelDown = FormMouseWheelDown
  OnMouseWheelUp = FormMouseWheelUp
  OnResize = FormResize
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 13
  object Image1: TImage
    Left = 264
    Top = 8
    Width = 225
    Height = 185
    OnClick = Image1Click
    OnMouseDown = FormMouseDown
    OnMouseUp = FormMouseUp
  end
  object Button1: TSpeedButton
    Left = 102
    Top = 7
    Width = 38
    Height = 23
    Caption = 'Draw'
    OnClick = Button1Click
  end
  object Button3: TSpeedButton
    Left = 102
    Top = 35
    Width = 19
    Height = 48
    Hint = 'Transform current cartesian coorditates to polar'
    Caption = #8595
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -11
    Font.Name = 'Tahoma'
    Font.Style = [fsBold]
    ParentFont = False
    OnClick = Button3Click
  end
  object Button2: TSpeedButton
    Left = 146
    Top = 7
    Width = 38
    Height = 23
    Caption = 'Reset'
    OnClick = Button2Click
  end
  object Button4: TSpeedButton
    Left = 102
    Top = 89
    Width = 19
    Height = 48
    Hint = 'Transform current polar coorditates to cartesian'
    Caption = #8593
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -11
    Font.Name = 'Tahoma'
    Font.Style = [fsBold]
    ParentFont = False
    OnClick = Button4Click
  end
  object Image2: TImage
    Left = 8
    Top = 143
    Width = 88
    Height = 25
    Hint = 
      'execute multiple Julia set drawing using source points from circ' +
      'le, moving by certain degree step'
    OnClick = Image2Click
  end
  object Shape1: TShape
    Left = 8
    Top = 174
    Width = 41
    Height = 27
    Hint = 'calculation time'
    Brush.Color = clBlue
  end
  object Label1: TLabel
    Left = 8
    Top = 180
    Width = 41
    Height = 13
    Hint = 'calculation time'
    Alignment = taCenter
    AutoSize = False
  end
  object SpeedButton1: TSpeedButton
    Left = 190
    Top = 8
    Width = 68
    Height = 23
    Hint = 'Save current image'
    Caption = 'Save image'
    OnClick = SpeedButton1Click
  end
  object SpeedButton2: TSpeedButton
    Left = 264
    Top = 8
    Width = 57
    Height = 23
    Hint = 'Save gif of multiple Julia sets if it is generated'
    Caption = 'Save GIF'
    OnClick = SpeedButton2Click
  end
  object Edit1: TEdit
    Left = 8
    Top = 8
    Width = 41
    Height = 21
    Hint = 'Number of max iterations'
    AutoSelect = False
    AutoSize = False
    NumbersOnly = True
    TabOrder = 0
    Text = '100'
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object Edit2: TEdit
    Left = 8
    Top = 35
    Width = 88
    Height = 21
    Hint = 'Real part, cartesian'
    AutoSelect = False
    AutoSize = False
    TabOrder = 1
    Text = '0'
    OnChange = Edit2Change
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object Edit3: TEdit
    Left = 8
    Top = 62
    Width = 88
    Height = 21
    Hint = 'Imaginary part, cartesian'
    AutoSelect = False
    AutoSize = False
    TabOrder = 2
    Text = '0'
    OnChange = Edit3Change
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object CheckBox2: TCheckBox
    Left = 127
    Top = 53
    Width = 13
    Height = 13
    Hint = 'Switch to Julia set, using source point specified in left fields'
    BiDiMode = bdLeftToRight
    Ctl3D = True
    ParentBiDiMode = False
    ParentCtl3D = False
    TabOrder = 3
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object ComboBox1: TComboBox
    Left = 55
    Top = 8
    Width = 41
    Height = 21
    Hint = 'Power of source polynome'
    Style = csDropDownList
    ItemIndex = 0
    ParentColor = True
    TabOrder = 4
    Text = '2'
    OnChange = ComboBox1Change
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
    Items.Strings = (
      '2'
      '3'
      '4'
      '5'
      '6')
  end
  object Edit4: TEdit
    Left = 8
    Top = 89
    Width = 88
    Height = 21
    Hint = 'r, polar'
    AutoSelect = False
    AutoSize = False
    TabOrder = 5
    Text = '1'
    OnChange = Edit4Change
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object Edit5: TEdit
    Left = 8
    Top = 116
    Width = 88
    Height = 21
    Hint = #966', polar'
    AutoSelect = False
    AutoSize = False
    TabOrder = 6
    Text = '0'
    OnChange = Edit5Change
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object Edit6: TEdit
    Left = 55
    Top = 177
    Width = 32
    Height = 21
    Hint = 'step for multiple Julia sets execution(as quarter of a degree)'
    AutoSelect = False
    AutoSize = False
    BiDiMode = bdRightToLeft
    NumbersOnly = True
    ParentBiDiMode = False
    TabOrder = 7
    Text = '4'
    OnKeyDown = FormKeyDown
    OnKeyUp = FormKeyUp
  end
  object Timer2: TTimer
    Enabled = False
    Interval = 50
    OnTimer = Timer2Timer
    Left = 160
    Top = 152
  end
  object Timer1: TTimer
    Enabled = False
    Interval = 40
    OnTimer = Timer1Timer
    Left = 112
    Top = 152
  end
  object Timer3: TTimer
    Enabled = False
    Interval = 10
    OnTimer = Timer3Timer
    Left = 208
    Top = 152
  end
  object XPManifest1: TXPManifest
    Left = 16
    Top = 224
  end
end
