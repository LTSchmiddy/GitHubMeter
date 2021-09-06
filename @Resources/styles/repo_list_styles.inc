[Variables]
fontName=Trebuchet MS
textSize=12
colorBar=235,170,0,255
colorText=255,255,255,205
colorTextDim=255,255,255,115
colorTextLCM=150,150,255,255

RepoNameStyle=styleRepoName
RepoDateStyle=styleRepoDate
RepoLCMStyle=styleRepoLCM
RepoLCAStyle=styleRepoLCA
offsetX = 0
offsetY = 40
spacingV = 10
entryW = 600
entryH = 40
; Name
entryNameX=15
entryNameY=0
entryNameW=250
entryNameH=20
; Date
entryDateX=30
entryDateY=25
entryDateW=350
entryDateH=20
; Commit Message
entryCommitMessageX=265
entryCommitMessageY=5
entryCommitMessageW=245
entryCommitMessageH=20
; Commit Author
entryCommitAuthorX=265
entryCommitAuthorY=25
entryCommitAuthorW=245
entryCommitAuthorH=20

[styleTitle]
StringAlign=Left
StringCase=Upper
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,50
FontColor=#colorText#
FontFace=#fontName#
FontSize=14
AntiAlias=1
ClipString=1

[styleRepoName]
StringAlign=Left
; Meters using styleLeftText will be left-aligned.
StringCase=None
; StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorText#
FontFace=#fontName#
FontSize=12
AntiAlias=1
ClipString=1

[styleRepoDate]
StringAlign=Left
StringCase=None
; StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorTextDim#
FontFace=#fontName#
FontSize=8
AntiAlias=1
ClipString=1

[styleRepoLCM]
StringAlign=Left
StringCase=None
; StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorTextLCM#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1

[styleRepoLCA]
StringAlign=Left
StringCase=None
; StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorTextDim#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1