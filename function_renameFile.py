import re


def checkForDups(tempList):  # List duplication checker
    seen = {}
    dupes = []
    for x in tempList:
        x = x.lower()
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    if str(dupes) == "[]":
        print("No Duplicates found")
    else:
        print("Duplicates found in List: " + str(dupes))


def renameFile(currentOS, filenameAndDirectory, filename, previousOutputFilename, dryRun):

    # Need to be able to handle triple digits eg ep 123

    removeStrings = [  # Remove all strings listed (Note: case and order doesn't matter)
        ".1080p.x265-ZMNT",
        "ZMNT",
        "[BD 2160p 4K UHD][HEVC x265 10bit][Dual-Audio][Multi-Subs]",
        "[BD 2160p 4K UHD]",
        "[HEVC x265 10bit]",
        " 4k ",
        " UHD",
        "2160p",
        "[]",
        "()",
        "{}",
        "[Web 1080p HEVC Multi]",
        "(1080p BluRay x265 HEVC 10bit EAC3 2.0 SAMPA)",
        "1080p.BluRay.AC3.x265.HEVC.10Mbit.HUN.ViZoZoN",
        "(Diamond Luxe)",
        "(1080p BluRay x265 HEVC 10bit EAC3 7.1 SAMPA)",
        "(1080p BluRay x265 HEVC 10bit EAC3 5.1 SAMPA)",
        "(1080p BluRay x265 HEVC 10bit AC3 1.0 SAMPA)",
        "(Criterion)(1080p BluRay x265 HEVC 10bit AC3 1.0 SAMPA)",
        "(1080p BluRay x265 HEVC 10bit AAC 7 1 SAMPA)",
        "(Criterion)",
        "HR-RG",
        "480p",
        "(Multiple Subtitle)",
        "[Multi-Subs]",
        "Web 1080p",
        "E-OPUS",
        "English-Dub",
        "HR-GZ",
        "HR-DR",
        "HR-SW",
        "[Eng-Subs] - Judas",
        "[BluRay 1080p HEVC]",
        "BD1080p",
        "[HEVC-x265]",
        "1080p.WEB.x264",
        "WEB.x264",
        "x264",
        "[x264]"
        "[BD]",
        "[AAC]",
        "Judas",
        "Erai-raws",
        "[TGx]",
        "(Dual Audio_10bit_BD720p_x265)",
        "[AkihitoSubs]",
        "[anime4life.]",
        "[HR]",
        "[JacobSwaggedUp]",
        "[kokus-rips]",
        "[Nep_Blanc]",
        "[ZRIPZ]",
        "[Cleo]",
        "[BD 1080p]",
        "[Opus]",
        "[10Bit]",
        "[x265]",
        "[HEVC]",
        "[BD 1920x1080 x265 10Bit Opus]",
        "(BD1080p AC3 10bit)",
        "Dual Audio",
        "Dual_Audio",
        "[x265_HEVC]",
        "(BD Batch + OVA)",
        "[1080p]",
        "(BD 1280x720)",
        "[Subbed]",
        "WEB.h264",
        "h264",
        "h265",
        "(1080p Bluray x265 HEVC 10bit AAC 5.1 Tigole)",
        "(1080p BluRay x265 HEVC 10bit AAC 7.1 Tigole)",
        "(1080p BluRay x265 10bit Tigole)",
        "1080p BluRay x265 HEVC EAC3-SARTRE [Torrent Downloads]",
        "(1080p BluRay x265 Silence)",
        "BDRip 1080p Ita Eng x265 - NAHOM",
        "[SEV]",
        "1080p",
        "DSNP",
        "WEBrip",
        "x265",
        "1080p NF WEBRip 10bit DD 5.1 x265.HEVC D0ct0rLew[UTR-HD]",
        "[UTR-HD]",
        "D0ct0rLew",
        "Diamond Edition 1080p 10bit Bluray x265 HEVC [Org DD 2.0 Hindi + DD 5.1 English] ESubs ~ TombDoc",
        "[Org DD 2.0 Hindi + DD 5.1 English]",
        "[1080p HEVC]",
        "10bit_BD720p_x265)",
        "BD720p",
        "[Pixel]",
        "[BDRip 1080p 10bit HEVC x265 Opus DualAudio(JPN ENG) Subbed Dubbed]",
        "BDRip",
        "Opus",
        "(JPN ENG)",
        "Subbed",
        "Dubbed",
        "[DB]",
        "[720p]",
        "(Dual Audio_10bit_BD1080p_x265)",
        "[Dual Audio 10bit 720p]",
        "[GSK_kun]",
        "[BDRip 1920x1080 x264 FLAC]",
        "(1920x1080 x265 flac)",
        "10-Bit",
        "YURASUKA",
        "BluRay",
        "FLAC2.0",
        "[Judas]",
        "[Kametsu]",
        "(BD 1080p Hi10 FLACx2)",
        "Hi10",
        "FLACx2",
        "[Nep_Blanc]"
        "MULTI VFF",
        "10Bits",
        "10Bit",
        "T0M",
        "ETTV",
        "BDRemux",
        "DVD",
        "WEB-DL",
        "[HorribleSubs]",
        "[AAC]"
        "ENG",
        "JPN",
        "[Aeenald]",
        "[ANE]",
        "[AnimeCreed]",
        "[BlurayDesuYo]",
        "[CBM]",
        "[Cerberus]",
        "[Chimera]",
        "[DragsterPS]",
        "[Multi-Audio]",
        "[Edge]",
        "[UNCENSORED BD 1080p]",
        "[HEVC-reencode]",
        "[DVDRip 1280x720 h264 ac3]",
        "DVDRip",
        "[HQR]",
        "[KgOlve]",
        "[KH]",
        "[Kōritsu_bonkai77]",
        "[neoHEVC]",
        "[Ranger]",
        "[Reaktor]",
        "[5.1]",
        "[Shisukon]",
        "[Tsundere]",
        "1024x576",
        "[VCB-Studio]",
        "[Ma10p_1080p]",
        "[Ma10p_720p]",
        "[wat15]",
        "[WBDP]",
        "[1080p-AC3-FLAC]",
        "8-bit FLAC 16-bit",
        "8-bit",
        "16-bit",
        "[ZetaRebel]",
        "720x480",
        "720x480p",
        "[sxales]",
        "(DVDRip 720x480p x265 HEVC AC3x3 2.0x3)",
        "(Hi10)",
        "(DVD_480p)",
        "(Exiled-Destiny)",
        "[Exiled-Destiny]",
        "(10bit_BD720p_x265)",
        "[Prof]",
        "HR-J",
        "[Dual-Audio]",
        "[BD 1080p AAC HEVC 10bit]",
        "[GrimRipper]",
        ".1080p.Blu-Ray.10-Bit.Dual-Audio.DTS-HD.x265",
        "DTS-HD",
        "iAHD",
        "(1080p BluRay x265 RCVR)",
        "(Dual Audio 10bit BD1080p x265)",
        "[Dual]",
        "[Subs]",
        "[HD]",
        "BrRip",
        "[Coalgirls-subs]",
        "Blu-Ray.10-Bit.Dual-Audio.TrueHD.x265",
        "TrueHD",
        "Blu-Ray",
        "[ShowY]",
        "[FFFmpeg]",
        "[BD 1080p HEVC AAC]",
        "[FFF]",
        "[Lazy Lily]",
        "[EMBER]",
        "[Mezashite]",
        "[BD 1080p AAC]",
        "FLACx2 2.0x2",
        "(Dual Audio)",
        "[cen]",
        "[Complete Subbed]",
        "WEB-720PX",
        "[Shinkiro-raw]",
        "[pkanime]",
        "[hshare.net]",
        "[ENG.SUBS]",
        "[UNCEN]",
        "[960x720]",
        "[EROBEAT]",
        "[UNCUT]",
        "[BDremux]",
        "( HT )",
        "[~AA~]",  # This need to be here for the ascii match below to work for some reason...
        "~AA~",    #
        u"\091" u"\126" u"\065" u"\065" u"\126" u"\093",  # Cant Match Tildes so Fuck You (Its equal to [~AA~])
        u"\126" u"\065" u"\065" u"\126",                  # ~AA~
        "[YTS.LT]",
        ".1080p.BluRay.x264-REGRET[EtHD]",
        "[EtHD]",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 Danish+Swedish Silence)",
        "1080p HEVC 10 Bit AC3 5.1 EN Subs EN",
        "BDRip.1080p.selezen",
        "(Dual Audio_10bit_BD720p)",
        "[DVDRip h264 720x480 10bit Vorbis]",
        "Vorbis"
        "[IMAX]",
        "WEB-DLRip.1080p",
        "WEB-DL.1080p",
        "[BDRip-1080p-MultiLang-MultiSub-Chapters][RiP By MaX]",
        "[RiP By MaX]",
        ".BDRip.1080p.Rus.Eng",
        ".ITA.ENG.BDrip.1080p.x264-Fratposa",
        "Fratposa",
        ".1080p.WEBRip.x264-ParovozN",
        "1080p.WEBRip.x264 - [YTS.AM]",
        "1080p.WEBRip.x264",
        "ParovozN",
        ".1080p.BDRip.10bit.x265.AC3",
        "AC3 5.1 ITA.ENG 1080p H265 sub ita.eng",
        "Sp33dy94-MIRCrew",
        ".x264.BDRip.(720p)-MediaClub",
        "MediaClub",
        ".x264.BDRip.1080p-MediaClub",
        "[1080p x265 HEVC 10bit BluRay AAC]",
        ".WEBRip.1080p.DUB+AVO",
        "DUB+AVO",
        "Bluray x265 10Bit AAC 5.1 - GetSchwifty",
        ".1080p.BluRay.10bit.HEVC.6CH-MkvCage.ws",
        "MkvCage",
        "[scy]",
        "Scy",
        ".iNTERNAL.720p.WEB.x264-GHOSTS",
        ".iNTERNAL.720p.WEB.x264-GHOSTS[eztv]",
        "[eztv]",
        ".720p.WEB.h264-TBS[eztv]",
        ".DVDRip.XviD-NYDIC",
        ".DVDRip.XviD-NYDIC.[UsaBit.com]",
        "[UsaBit.com]",
        "[ www.Torrent9.uno ]",
        ".FASTSUB.VOSTFR.WEBRip.XviD.EXTREME",
        ".iNTERNAL.480p.x264-mSD[eztv]",
        ".iNTERNAL.480p.x264-mSD",
        ".720p.WEB.x265-MiNX[eztv]",
        ".720p.WEB.x265-MiNX",
        ".720p.WEB.x265",
        ".1080p.HDTV.x264-FaiLED[rarbg]",
        "[rarbg]",
        "FaiLED",
        "(1080p AMZN WEB-DL x265 HEVC 10bit AAC 2.0 Panda)",
        ".1080p.BluRay.10Bit.HEVC.EAC3-SARTRE",
        ".1080p.NF.WEBRip.DD5.1.x264-Morpheus",
        ".OAR.1080p.BluRay.x264-HD4U[rarbg]",
        "[480p]",
        "[DVD]",
        "[pseudo]",
        "[YTS.AG]",
        "Criterion (1080p BluRay x265 HEVC 10bit AAC 5.1 Tigole)",
        "720p HDTV 2CH x265 HEVC-PSA",
        "(1080p AMZN WEB-DL x265 HEVC 10bit EAC3 6.0 RZeroX)",
        ".BluRay.x264.AC3-ETRG",
        "(1080p DSNYP Webrip x265 10bit EAC3 5.1 Atmos - Goki)",
        "(1080p BluRay x265 HEVC 10bit DTS 5.1 Qman) [UTR]",
        "[UTR]",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 RCVR)",
        "720p BluRay x264 [i_c]",
        "[i_c]",
        "(1080p AMZN WEB-DL x265 HEVC 10bit DDP 5.1 Vyndros)",
        "1080p 10bit NF WEB-RIP x265 [Hindi DD 640Kbps Org 5.1 - Eng DD 2.0] ~ EmKayy",
        "[Hindi DD 640Kbps Org 5.1 - Eng DD 2.0]",
        "EmKayy",
        ".1080p.BluRay.H264.AAC-RARBG",
        ".1080p.WEBRip.DD5.1.x264-CM",
        ".HDTV.h264-SFM[rartv]",
        ".720p.x265-MeGusta",
        "1080p Genuine BD Rip HEVC 2-Pass 10 Bit AC3 5.1 EN Sub",
        "1080p Webrip x265 AC3 5.1 Goki [SEV]",
        ".1080p.WEBRip.x264-XLF[TGx]",
        ".1080p.CBS.WEBRip.AAC2.0.x264-TEPES[TGx]",
        ".1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb[TGx]",
        "-MEECH",
        ".Bluray.TrueHD-7.1-Grym",
        "(1080p DSNYP Webrip x265 10bit EAC3 5.1 - Goki)[TAoE]",
        "Mp4 x264 AC3 1080p",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)",
        "(1080p BluRay x265 HEVC 10bit DTS 7.1 Qman) [UTR]",
        ".1080p.AMZN.WEBRip.DDP5.1.x265-SiGMA[rartv]",
        "Mp4 1080p",
        "(1080p BDRip x265 10bit EAC3 5.1 - Goki)[TAoE]",
        "[TAoE]",
        ".1080p.BluRay.x265-RARBG",
        "RARBG",
        "-RARBG",
        ".PROPER.1080p.BluRay.H264.AAC-RARBG",
        "1080p NF Webrip x265 10bit EAC3 5.1 - Ainz",
        "BDRip 1080p x264 AAC - KiNGDOM",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 RZeroX)",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 afm72)",
        "(1080p BluRay x265 HEVC 10bit AAC 7.1 Korean Silence)",
        "1080p 10 bit x264- Obey",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 FreetheFish)",
        ".1080p.AMZN.WEBRip.DDP2.0.x264-NTb",
        "(1080p BluRay x265 HEVC 10bit AC3 5.1 Chinese SAMPA)",
        "1080p.BluRay.x264-HD4U",
        ".HDTV.x264-SVA[ettv]",
        "720p.HDTV.x265-MiNX[TGx]",
        ".WEBRip.x264-ION10",
        ".WEB.h264-TBS[ettv]",
        "(1080p DS4K RED WEB-DL x265 HEVC 10bit AAC 5.1 Vyndros)",
        "(1080p BluRay x265 HEVC 10bit AAC 2.0 Vyndros)",
        ".1080p.NF.WEBRip.DDP5.1.Atmos.x264-NTG[TGx]",
        "720p BluRay x264 300MB Pahe.in",
        ".1080p.HQ.10bit.BluRay.5.1.x265.HEVC-MZABI",
        "BluRay x265 10Bit HEVC [English DD 5.1 640 Kbps] [Dzrg Torrents®]",
        ".1080p.WEB.H264-ANTAGONiST[rarbg]",
        ".1080p.DCU.WEB-DL.DDP5.1.H264-NTb[TGx]",
        ".1080p.DCU.WEBRip.DDP5.1.x264-NTb[rarbg]",
        ".1080p.BluRay.x264-SHORTBREHD[rartv]",
        ".1080P.DVDScr.X264.AC3.SHQ.Hive-CM8[TGx]",
        ".1080p.WEB.H264-METCON[TGx]",
        ".PROPER.1080p.WEB.H264-ELiMiNATE[TGx]",
        ".1080p.WEB-DL.DD5.1.H264-TOMMY[TGx]",
        ".1080p.WEB-DL.DD5.1.H264-BTN[TGx]",
        "(1080p ATVP Webrip x265 10bit EAC3 5.1 Atmos - Goki)",
        ".1080p.BluRay.x265.HEVC.EAC3-SARTRE",
        ".720p.HDTV.TNT",
        ".1080p.BluRay.x265.HEVC.10bit.5,1ch(xxxpav69)",
        "(xxxpav69)",
        "BR EAC3 VFF ENG 1080p x265 10Bits T0M",
        "BR EAC3 VFF VFQ ENG 1080p x265 10Bits T0M",
        ".1080p.AMZN.WEBRip.DDP5.1.x264-TEPES[rarbg]",
        "[YTS.AM]",
        "-Judas[TGx]",
        ".1080p.BluRay.x264.AC3-DDL",
        "(1080p AMZN Webrip x265 10bit EAC3 5.1 - Goki)",
        "1080p 10bit Bluray x265 HEVC [Org DD 5.1 Hindi + DD 5.1 English] ESub ~ TombDoc",
        "(1080p Bluray x265 HEVC 10bit AAC 5.1 Swedish Tigole)",
        "(BD 1080p)(HEVC x265 10bit)(Multi-Subs)-Judas[TGx]",
        "_(10bit_BD1080p_x265)",
        "(10bit_BD1080p_x265)",
        "(480p DVD x265 HEVC 10bit DD5.1 Vyndros)",
        ".WS.1080p.BluRay.x264.DTS-FGT",
        ".1080p.BluRay.x264-TheWretched [PublicHD]",
        "[PublicHD]",
        ".1080p.BluRay.x264-SONiDO [PublicHD]",
        ".BluRay.1080p.DTS.x264.Millie.Bobby.Brown",
        ".DVD9",
        "DVD9",
        ".720p.HDTVRip",
        ".1080p.WEBRip.x264-RARBG",
        "(BD Batch)",
        "HR-SR",
        "[infanf]",
        "[ASW]",
        "[LowPower-Raws]",
        "(BD 1080P x265 Ma10p FLACx3)",
        "[Moozzi2]",
        "(BD 1920x1080 x265-10Bit Flac)",
        "[Anime Time]",
        "[AnimeRG]",
        "(Batch)",
        "[HEVC x265 8bit]",
        "ITA WEBRip 1080p x265 mkv - iDN CreW",
        "(Batch) v2",
        "[v2]"
        "[AnimeKayo]",
        "[Marshall]",
        "[kmplx]",
        "(BD 1080p x265 10-Bit Opus)",
        "[FY-Raws]",
        "[FuniDub 1080p x265 AAC]",
        ".1080p.Blu-Ray.10-Bit.Dual-Audio.DTS-HD.x265-iAHD",
        "[DavRips]",
        "[Web-Rip 1080p x265 10 bit]",
        "VOSTFR",
        "[Kaerizaki]",
        "(Weekly)",
        "(DVDRip Hi10 768x576 x265)",
        "SubsPlease]",
        "WEB-DLRip",
        "[Ohys-Raws]",
        "(AT-X 1280x720 x264 AAC)",
        "(TBS 1280x720 x264 AAC)",
        "[SubsPlease]",
        "(BD 1280x720 x264 AACx2)",
        "(BS11 1280x720 x264 AAC)",
        "(CX 1280x720 x264 AAC)",
        "[Multiple Subtitle] ",
        "[Erai-raws] ",
        "Ohys-Raws]",
        "(BD 1920x1080 x264+ FLACx2)",
        "(MX 1280x720 x264 AAC)",
        "(CX 1920x1080 x264+ AAC)",
        ".1080p.H264.ita.jpn.Ac3.sub.ita-MIRCrew",
        "(720p)(Multiple Subtitle)-Erai-raws[TGx]",
        "(480p)(Multiple Subtitle)-Erai-raws[TGx]",
        "HDRip] Dub",
        "HDRip",
        "720p DUAL AUDIO x264",
        "[NEW]",
        "[Hentai 2D]",
        "[UNCENSORED]",
        "[WEBRip 1080p]",
        "[Halfwitsubs]",
        "[Baha]",
        "[WEB-DL]",
        "[AVC AAC]",
        "[CHT]",
        "[MP4]",
        " DC ",
        "Open Matte",
        "UNRATED",
        "ITA-JAP Ac3 5.1 BDRip 1080p H264 [ArMor]",
        "ITA-JAP",
        "[WEBRip 1080p HEVC]",
        "[Hindi Dub] h.264 Dual-Audio AAC x264",
        "Hindi Dub]",
        "h.264",
        "(540p)",
        "1080p BluRay DUAL AUDIO x264",
        "[ArMor]",
        "iDN CreW",
        "ITA AC3 WEBRip H264 - L@Z59",
        "[BDRip 1080p]",
        "[Batch]",
        "[H.265 10bit]",
        "[CuaP] ",
        "[mal lu zen]",
        "[Hakobune]",
        "[1080p x265]",
        "[1080p x265][Raw with JP Subs - Netflix] HR-MF",
        "[Raw with JP Subs -Netflix]",
        "HR-MF",
        "[1080p BDRemux x265 DTS-HD MA 5.1]",
        "[1080p BDRemux x265 DTS-HD MA 5.1] HR-MF",
        "FullHD x265",
        "[MiniFreeza]",
        "1080p BDRip 10 bits AAC x265-EMBER",
        "1080p Dual Audio BDRip 10 bits DD x265-EMBER",
        "[Eng-Subs]",
        "[JesuSub] vostfr 720p x265 AAC",
        "x265 10bits PTBR",
        "[1080P_x265(10bit)-FLAC][ALL]",
        "1080P HEVC 8Bit X265",
        "[Skytree]",
        "[CRRIP]",
        "[JesuSub]",
        "(DVDRip 768x576 x265 AC3)",
        "(DVDRip 1024x576 x265 FLAC)",
        "[Maximus]",
        "[Noob-Subs]",
        "CBM]",
        "(WEBDL) 1080p x265 Ukr DVO",
        "(WEBDL)",
        "Eng-Subs",
        "[YTS AM]",
        "[Blu Ray]",
        "[1080p][BD][x265][10-bit][Dual-Audio]",
        "[SAIO Raws]",
        "[BD 1920x1080 HEVC 10bit OPUS]",
        "[eng subbed]{Neroextreme}_NTRG",
        "[eng subbed]",
        "[rich_jc]",
        "BD 1080p 8bit [rich_jc]",
        "1920x1080 Blu ray FLAC",
        "Blu ray",
        "[ShadyCrab 1080p 8bit AAC] [Dual Audio]",
        "[zza]",
        "[1080p.x265][multisubs:eng,fre][Vostfr]",
        "[1080p.x265]",
        "[multisubs:eng,fre]",
        "[Delivroozzi]",
        "[VOSTFR BD x264 10bits 1080p FLAC]",
        ".JPN.UHD.BluRay.x265.HDR.DDP.5.1.MSubs-DTone",
        "[HDR]",
        "(HDR)",
        "[CHiP] ",
        "[japanese]",
        "[LWND]",
        "1080p.x264.AAC ENG Subs",
        "[35mm]",
        "[BD 1920x1036 HEVC 10bit OPUSx2]",
        "10 bit 1080p HEVC BDRip [MOVIE]",
        "[MOVIE]",
        "(BD 1920x1036 x 265 10Bit 4Audio) Movie Tokuten BD",
        "[BDRip 1036p x264 FLAC]",
        ".1080p.10bit.DSNP.WEB-DL.DDP5.1.HEVC-Vyndros",
        "(1080p BDRip x265 10bit EAC3 5.1 - Erie)[TAoE]",
        "(1080p x265 10bit Tigole)",
        "(1080p BDRip x265 10bit EAC3 5.1 - xtrem3x) [TAoE]",
        ".1080p.10bit.BluRay.x265.HEVC.6CH-MRN",
        ".1080p.WEB-DL.x265.10bit.EAC3.2.0-Qman[UTR]",
        "Ita Eng x265-NAHOM",
        "[Beatrice-Raws]",
        "[AniFilm]",
        "[HDRip][MVO]",
        "[Nemuri]",
        "[SEKAI PROJECT]",
        "HEVC AC3 5.1",
        "[YnK]",
        "[BD 1036p]",
        "1036p",
        "1080p NF WEBRip DD5.1 x264-QOQ",
        "1080p WEBRip x264-STRiFE",
        "VOSTFR 1080p NF WEBRip DD5.1 x264-QOQ",
        "720p WEBRip XviD AC3-FGT",
        "FRENCH WEBRip NF XviD-GZR",
        "VOSTFR WEBRip XviD AC3-ACOOL",
        "WEBRip XviD AC3-FGT",
        "FRENCH WEBRip NF x264-LiBERTAD",
        "MULTI 1080p WEBRip x264-ACOOL",
        "-ACOOL",
        "WEBRip x264-FGT",
        "[YIFY]",
        "[YTS]",
        "720p BluRay x264-W4F [RiCK]",
        "[RiCK]",
        "[5 1]",
        "[RAW]",
        "[RUS+JAP]",
        "h.265",
        "[h.265]",
        "[bonkai77]",
        "Dual.Audio.Bluray",
        "(1080p BluRay x265 ImE)",
        "TVRip x265 ImE",
        "(Pilot)",
        "TVRip",
        "(480p TVRip x265 ImE)",
        "(1080p WEB-DL x265 ImE)",
        "[1080p x265 HEVC 10bit BD Dual Audio AAC 5.1] [Prof]",
        "[1080p x265 HEVC 10bit BD Dual Audio AAC 5.1]",
        "1080p HEVC AC3 5.1",
        "[1080p x265 q22",
        "[1080p AI x265",
        "[1080p x265 10bit",
        "[1080p AI x265 10bit",
        "[1080p x265 10bit Joy]",
        "(1080p x265 q22 Joy)",
        "(1080p x265 10bit Joy)",
        "(1080p BD x265 10bit",
        "(1080p AMZN x265 10bit",
        "(1080p x265 10bit",
        "(1080p x265 q23",
        "(1080p x265 q22",
        "(1080p x265 q21",
        "(1080p x265 q20",
        "(1080p x265 q19",
        "(1080p x265 q18",
        "(1080p x265 HEVC AAC 5.1 Joy)",
        "[2160p x265 q22",
        "[2160p AI x265",
        "[2160p x265 10bit",
        "[2160p AI x265 10bit",
        "[2160p x265 10bit Joy]",
        "(2160p x265 q22 Joy)",
        "(2160p x265 10bit Joy)",
        "(2160p BD x265 10bit",
        "(2160p AMZN x265 10bit",
        "(2160p x265 q23",
        "(2160p x265 q22",
        "(2160p x265 q21",
        "(2160p x265 q20",
        "(2160p x265 q19",
        "(2160p x265 q18",
        "(2160p x265 HEVC AAC 5.1 Joy)",
        "1080p 10bit Bluray x265 HEVC English DDP 5.1 ESub ~ TombDoc",
        "TombDoc",
        "2160p NF WEBRip NVENC HEVC 10bit AAC 5 1 Joy UTR",
        "2160p NF WEBRip NVENC HEVC 10bit AAC 5 1 Joy",
        "1080p NF WEBRip NVENC HEVC 10bit AAC 5 1 Joy",
        "2160p AMZN WEB DL AI x265 HEVC 10bit AAC 5 1 Joy UTR",
        "2160p AMZN WEB DL AI x265 HEVC 10bit AAC 5 1 Joy",
        "1080p AMZN WEB DL AI x265 HEVC 10bit AAC 5 1 Joy",
        "(2160p AMZN WEB-DL AI x265 HEVC 10bit AAC 5 1 Joy)",
        "(1080p AMZN WEB-DL AI x265 HEVC 10bit AAC 5 1 Joy)",
        "(1080p BDRip x265 10bit EAC3 5.1 - Species180) [TAoE]",
        "(1080p BDRip x265 10bit EAC3 5.1 - Species180)",
        "(1080p WEB-DL x265 Panda)",
        "(Bd 1080P Hi10 Flac)",
        "EAC3",
        "Theatrical",
        "Theatrical Cut",
        "Directors",
        "Directors Cut",
        ]

    # simpleList = [
    # "AMZN",
    # "WEB DL",
    # "x265",
    # "x264",
    # "HEVC",
    # "AVC",
    # "10bit",
    # "AAC",
    # "EAC3",
    # "5.1",
    # "2.0",
    # "BD",
    # "Dual Audio",
    # "TVRip",
    # "480p",
    # "720p",
    # "Bluray",
    # "Dual.Audio",
    # "h.265",
    # "5 1",
    # "WEBRip",
    # "MULTI",
    # "AC3",
    # "XviD",
    # "VOSTFR",
    # "DD5.1",
    # "NF",
    # "1036p",
    # "HDRip",
    # "1920x1036",
    # "1920x1080",
    # "BDRip",
    # "OPUS",
    # "HDR",
    # "UHD",
    # "2160p",
    # "8bit",
    # "FLAC",
    # "Blu ray",
    # "eng subbed",
    # "WEBDL",
    # "WEB-DL",
    # "1024x576",
    # "768x576",
    # "576p",
    # "FullHD",
    # "UltraHD",
    # "BDRemux",
    # "DTS-HD",
    # "Netflix",
    # "H264",
    # "1280x720",
    # "WEB-DLRip",
    # "Hi10",
    # "DVDRip",
    # "HDTVRip",
    # "DVD9",
    # "DVD",
    # "DTS",
    # "TrueHD",
    # "Blu-Ray",
    # "16-bit",
    # "WEB",
    # "Multi"
    # ]

    # List duplication checker :)
    #checkForDups(removeStrings)

    removeStringsSorted = (sorted(removeStrings, key=len, reverse=True))

    #for item in removeStringsSorted:
    #    print(item)

    #breakpoint()

    outputFilename = filename[:-4]  # Remove last 4 characters = .mkv or .mp4 etc

    for item in removeStringsSorted:
        if not outputFilename.find(item)+len(item) == len(item) - 1:
            # covert strings to lowercase, why? because re.sub and []() don't work together
            outputFilenameLower = outputFilename.lower()
            itemLower = item.lower()
            print(item)
            # Beautiful, we don't work on the actual filename, so original uppercase and lowercase is unchanged
            # only subtracting the positions
            outputFilename = outputFilename[:outputFilenameLower.find(itemLower)] + outputFilename[outputFilenameLower.find(itemLower) + len(item):]

    outputFilename = re.sub("FS[0-9][0-9] Joy]", "", outputFilename, flags=re.I)           # Take this joy
    outputFilename = re.sub("FS[0-9][0-9] Joy\)", "", outputFilename, flags=re.I)           # And your dumb filenames
    outputFilename = re.sub("FS[0-9][0-9][0-9] Joy\)", "", outputFilename, flags=re.I)      # Yes i did write a regex
    outputFilename = re.sub("FS[0-9][0-9][0-9] Joy]", "", outputFilename, flags=re.I)      #
    outputFilename = re.sub("S[0-9][0-9] Joy\)", "", outputFilename, flags=re.I)            # for one person
    outputFilename = re.sub("S[0-9][0-9] Joy\)", "", outputFilename, flags=re.I)            #
    # match = 0
    # firstMatchText = ""
    # secondMatchText = ""
    # for item in simpleList:  # The Terminator, if brute force won't work, then well have to rely on smarts.
    #    if outputFilename.find(item) != -1:  # If it finds like x265 and Hi10 between two brackets it will remove it.
    #        match += 1
    #        if match == 1:
    #            firstMatchText = item
    #        elif match == 2:
    #            secondMatchText = item
    #            inputLen = len(outputFilename)
    #            matching = r"\(.*(" + firstMatchText + r").*(" + secondMatchText + r").*\)"
    #            outputFilename = re.sub(matching, "", outputFilename)
    #            matching = r"\[(].*(" + firstMatchText + r").*(" + secondMatchText + r").*\]"
    #            outputFilename = re.sub(matching, "", outputFilename)
    #            if inputLen == len(outputFilename):  # Flip the secondMatchText and firstMatchText
    #                matching = r"\(.*(" + secondMatchText + r").*(" + firstMatchText + r").*\)"
    #                outputFilename = re.sub(matching, "", outputFilename)
    #                matching = r"\[(].*(" + secondMatchText + r").*(" + firstMatchText + r").*\]"
    #                outputFilename = re.sub(matching, "", outputFilename)
    #            break

    outputFilename = re.sub("\[[^\[][^\[][^\[][^\[][^\[][^\[][^\[][^\[]]", "", outputFilename, flags=re.I)  # remove e.g.[ABC12345]
    outputFilename = re.sub("\([^\[][^\[][^\[][^\[][^\[][^\[][^\[][^\[]\)", "", outputFilename, flags=re.I)  # remove e.g.(ABC12345)

    #outputFilename = re.sub("\.$", "", outputFilename)
    #print(re.search("\.$", outputFilename))

    if not re.search("S[0-9][0-9]E[0-9][0-9].[0-9] ", outputFilename):  # If S01E01.5(space), then skip removing dots (Some use the .5 for a second part of an episode)
        if outputFilename.count(".") >= 2 and re.search("\.$", outputFilename) is None:  # if theres 2 or more dots
            outputFilename = outputFilename.replace(".", " ")  # _ is usually a stand in for a space
    outputFilename = re.sub("\.$", "", outputFilename)
    outputFilename = outputFilename.replace("_", " ")  # _ is usually a stand in for a space

    outputFilename = re.sub("\s\s+", " ", outputFilename)  # Make 2 or more continuous spaces into one

    outputFilename = outputFilename.replace("( )", "")  # Remove empty brackets
    outputFilename = outputFilename.replace("[ ]", "")  # Remove empty brackets



    import datetime
    now = datetime.datetime.now()

    currentDecade = str(now.year)[2]
    currentYear = str(now.year)[3]

    # Remove numbers 1920 to current year

    outputFilename = re.sub(r"\s20[0-" + currentDecade + "][0-" + currentYear + "]", "", outputFilename)
    outputFilename = re.sub(r"\s20[0-1][0-9]", "", outputFilename)
    outputFilename = re.sub(r"\s19[2-9][0-9]", "", outputFilename)

    outputFilename = re.sub("\([0-9][0-9][0-9][0-9]\)", "", outputFilename)  # Remove Years eg. (1994) NOTE: Don't remove years with spaces on both sides
    outputFilename = re.sub("\[[0-9][0-9][0-9][0-9]]", "", outputFilename)  # [1994]


    outputFilename = re.sub(r"ep ([0-9][0-9])", r"E\1", outputFilename, flags=re.I)  # ep 13 to E13
    outputFilename = re.sub(r"ep ([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep 3 to E03
    outputFilename = re.sub(r"Episode ([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep 3 to E03

    outputFilename = re.sub(r"ep([0-9][0-9])", r"E\1", outputFilename, flags=re.I)  # ep03 to E03
    outputFilename = re.sub(r"ep([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep3 to E03 Haven't seen one with this case, but il code it in anyway

    outputFilename = re.sub("- ([0-9][0-9][0-9])$", r" E\1 ", outputFilename)  # Replace "- 001" with E001, why would any have so may episodes, IDK
    outputFilename = re.sub("-([0-9][0-9])$", r" E\1 ", outputFilename)  # Replace -01 If at end of file name
    outputFilename = re.sub("\[([0-9][0-9])]", r" E\1 ", outputFilename)  # Replace [01] with E01

    outputFilename = re.sub("([0-9][0-9])x([0-9][0-9])", r" S\1E\2 ", outputFilename, flags=re.I)  # 11x01 to S11E01
    outputFilename = re.sub("([0-9])x([0-9][0-9])", r" S0\1E\2 ", outputFilename, flags=re.I)  # 1x01 to S01E01

    outputFilename = re.sub("(S[0-9][0-9]E[0-9][0-9]) -", r"\1", outputFilename, flags=re.I)  # Removes space + Hyphen (S11E01 -)
    outputFilename = re.sub(" - (S[0-9][0-9]E[0-9][0-9])", r" \1", outputFilename, flags=re.I)  # Removes space + Hyphen + space ( - S11E01) to ( S11E01)

    outputFilename = outputFilename.replace(" -", " ")
    outputFilename = outputFilename.replace("- ", " ")

    outputFilename = re.sub("\s\s+", " ", outputFilename)  # Make 2 or more continuous spaces into one, yes we do this twice
    outputFilename = outputFilename.strip()  # Remove leading and trailing whitespaces
    outputFilename = re.sub("\s([0-9][0-9])\s", r" E\1 ", outputFilename)  # Replace (space + 02 + space) If there are double digits left at is stage this its probably an Ep number

    if re.search("\s[0-9]{2}$", outputFilename):
        if previousOutputFilename[:-2] == (re.sub("\s([0-9][0-9])$", r" E\1 ", outputFilename).strip())[:-2]:  # Optimize if everything but the last two characters are the same
            outputFilename = re.sub("\s([0-9][0-9])$", r" E\1 ", outputFilename)
        else:
            from function_getRuntime import getRuntime
            if getRuntime(currentOS, filenameAndDirectory, filename) < 4001:  # if over 1.1 hours long, its probably not an episode
                outputFilename = re.sub("\s([0-9][0-9])$", r" E\1 ", outputFilename)  # If there are two digits at the end of the filename, then there probably an episode number, only on .mkv files

    outputFilename = outputFilename.strip()  # Remove leading and trailing whitespaces
    outputFilename += ".mkv"  # Add extension

    #print(outputFilename)

    return outputFilename
