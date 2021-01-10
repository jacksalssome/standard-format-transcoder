from prettytable import PrettyTable
from compareSizes import compareSizes


def main2(filename, metadataTable, totalNumOfStreams, currentOS, removeSubsIfOnlyEngAudio):

    # Overview:

    # Get the pretty table and read each row, create variables for each column. Check variable for relevant info.
    # First for loop handles metadata entry, sets defaults streams
    # Second for loop handles mapping so we don't copy over wanted streams and handles minimum amount or streams.

    #print("Started main2")

    mapThisStream = ""  # Don't add streams non eng/jpn streams
    outputStreamNum = 0  # apply the metadata to the final stream number for ffmpeg will forget when it maps the streams "Stream #0:12 -> #0:3 (copy)"

    # Check language tags and titles for a language, if one
    # is found then add on the audio type eg. English (stereo)
    defaultSubSelected = False  # Becomes True when a Default Sub stream is selected
    defaultAudioSelected = False  # Becomes True when a Default Audio stream is selected

    numOfAudioStreams = 0  # Make sure theres at
    firstAudioStreamNum = -1  # lease one Audio Track
    signSongsSubStream = -1
    firstAudioStreamMap = ""  # For adding sub/signs if its the only sub track
    lineNum = 0
    metadataOptions = ""
    numOfEngSubs = 0  # For selecting the biggest eng sub stream
    engDefaultSubSelectorString = ""
    engSubStreams = ""
    startofengstreams = 0
    currentStreamNum = 0
    mapThisStreamIfNoSubsFound = ""

    # For removeSubsIfOnlyEngAudio
    numOfEngAudio = 0
    numOfJpnAudio = 0
    shadowMetadataOptions = ""
    shadowMapThisStream = ""

    metadataTable2 = PrettyTable(['Index', 'title', 'language', 'codec_type', 'channels'])  # Output Table
    permTitleLang = ""
    PermThisStreamLanguage = ""
    PermMetaCodecType = ""
    permMetaChannels = ""

    for line in range(0, totalNumOfStreams):
        titleLang = "\""  # So i don't have to escape so many times (Theres only one titleLand per loop)
        addAudioInfo = False
        aLanguageWasFound = False
        thisStreamLanguage = "und"
        mapTheSignsSongsStream = False
        isASignSongsSubStream = False
        makeThisSubDefault = False

        # Populate temp variables with data from prettytable
        metaTitle = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["title"]).strip()).lower()  # .lower() for case insensitive
        metaLang = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["language"]).strip()).lower()
        metaCodecType = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_type"]).strip()).lower()
        metaChannels = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["channels"]).strip()

        #print(metaTitle)
        #print(metaLang)
        #print(metaCodecType)
        #print(metaChannels)

        #print(str(lineNum)+": "+metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["language"]).strip())

        # Handles Audio and subtitles

        if metaTitle.find("signs") != -1 or metaTitle.find("songs") != -1:  # Looking for song/signs
            metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " title=\"Signs / Songs\"")
            signSongsSubStream = lineNum
            isASignSongsSubStream = True
            aLanguageWasFound = True
            mapTheSignsSongsStream = True
        elif metaLang == "eng":
            titleLang += "English"
            thisStreamLanguage = "eng"
            addAudioInfo = True
            aLanguageWasFound = True
            if metaTitle.find("full subs") != -1 or metaTitle.find("full subtitle") != -1 and defaultSubSelected is False:  # if the sub's title is "full subs", then we found your default
                makeThisSubDefault = True
                defaultSubSelected = True
        elif metaLang == "jpn":
            titleLang += "Japanese"
            thisStreamLanguage = "jpn"
            addAudioInfo = True
            aLanguageWasFound = True

        if aLanguageWasFound is False:  # If theres no audio tags then check the streams title
            if metaTitle.find("english") != -1 or metaTitle.find("inglês") != -1:
                titleLang += "English"
                thisStreamLanguage = "eng"
                addAudioInfo = True
                print("Found Title Via Backup way")

            elif metaTitle.find("japanese") != -1 or metaTitle.find("Japonês") != -1:
                titleLang += "Japanese"
                thisStreamLanguage = "jpn"
                addAudioInfo = True
                print("Found Title Via Backup way")

        if addAudioInfo is True:
            if metaChannels == "2":
                titleLang += " (2.0)"
            elif metaChannels == "6":
                titleLang += " (5.1)"
            elif metaChannels == "8":
                titleLang += " (7.1)"

        # Default streams

        if defaultAudioSelected is False and metaCodecType == "audio" and thisStreamLanguage == "jpn":  # Check if first Jap Audio and set as default
            defaultAudioSelected = True
            numOfAudioStreams += 1
            metadataOptions += " -disposition:" + str(outputStreamNum) + " default"
        elif metaCodecType == "audio" and defaultAudioSelected is False:  # Stop FFmpeg from making the first audio stream default
            metadataOptions += " -disposition:" + str(outputStreamNum) + " 0"

        if defaultSubSelected is False and metaCodecType == "subtitle" and thisStreamLanguage == "eng" and defaultAudioSelected == True:  # Check if first Eng Sub and set as default
            #defaultSubSelected = True
            if startofengstreams == 0:
                startofengstreams = lineNum
            if isASignSongsSubStream == False:  #Song / Signs is not an Eng Sub
                numOfEngSubs += 1
            engSubStreams += str(lineNum) + "|"
            engDefaultSubSelectorString = " -disposition:" + str(outputStreamNum) + " default"
        elif defaultSubSelected is False and metaCodecType == "subtitle" and thisStreamLanguage == "und":
            mapThisStreamIfNoSubsFound += str(lineNum) + " "
        elif metaCodecType == "subtitle" and makeThisSubDefault is False:  # Stop FFmpeg from making the first sub stream default
            metadataOptions += " -disposition:" + str(outputStreamNum) + " 0"
        elif makeThisSubDefault is True:
            metadataOptions += " -disposition:" + str(outputStreamNum) + " default"  # "full subs" found, make it default
            makeThisSubDefault = False

        titleLang += "\""  # zip up titleLang

        if mapTheSignsSongsStream == True:  # Map Songs/signs
            mapThisStream += str(lineNum) + " "
            outputStreamNum += 1

        if thisStreamLanguage != "und":  # Don't title non eng/jpn (all stream com in as und and were renamed earlier)
            if metaCodecType != "video":  # Don't title video streams

                metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " title=" + titleLang)
                metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " language=" + thisStreamLanguage)

                mapThisStream += str(lineNum) + " "
                outputStreamNum += 1

        if metaCodecType.find("video") != -1:  # Add the video stream
            mapThisStream += str(lineNum) + " "
            shadowMapThisStream += str(lineNum) + " "
            outputStreamNum += 1

        if metaCodecType == "audio" and firstAudioStreamNum == -1:
            firstAudioStreamMap = str(outputStreamNum) + "( "
            firstAudioStreamNum = lineNum

        if metaLang == "eng" and metaCodecType == "audio":
            numOfEngAudio += 1
            shadowMapThisStream += str(lineNum) + " "
            shadowMetadataOptions += (" -metadata:s:" + str(outputStreamNum - 1) + " title=" + titleLang)
        if metaLang == "jpn" or metaTitle.find("japanese") != -1 and metaCodecType == "audio":
            numOfJpnAudio += 1

        #print(metadataOptions)
        #print(outputStreamNum)

        # -- remove mjpeg video streams --

        lineNum += 1

        permMetaChannels = metaChannels
        permTitleLang = titleLang
        PermMetaCodecType = metaCodecType
        PermThisStreamLanguage = thisStreamLanguage

        if titleLang == "\"\"" or metaCodecType == "video":
            permTitleLang = ""
        if thisStreamLanguage == "und" or metaCodecType == "video":
            PermThisStreamLanguage = ""
        if mapTheSignsSongsStream == True:
            permTitleLang = "Signs / Songs"
        #if metaChannels == "":
        #    permMetaChannels



        if outputStreamNum > currentStreamNum:
            currentStreamNum = outputStreamNum

            metadataTable2.add_row([outputStreamNum - 1, permTitleLang.replace("\"", ""), PermThisStreamLanguage, PermMetaCodecType, permMetaChannels])
            permTitleLang = ""
            PermThisStreamLanguage = ""
            PermMetaCodecType = ""
            permMetaChannels = ""

    # Select the second biggest subtitle by filesize and set it as default
    # second biggest because there might be a close caption
    if numOfEngSubs == 0:
        mapThisStream += mapThisStreamIfNoSubsFound
    elif numOfEngSubs == 1 and defaultSubSelected is False:  # set default if theres only one eng sub
        metadataOptions += engDefaultSubSelectorString
        defaultSubSelected = True
        #print(engDefaultSubSelectorString)
        #print(numOfEngSubs)
    elif numOfEngSubs > 1 and defaultSubSelected is False:  # If we found an eng track with title including "full subs" its already default
        lineNum = startofengstreams

        #print("here2")
        biggestStreamSize = 0
        biggestStreamNum = 0
        secondBiggestStreamSize = 0
        secondBiggestStreamNum = 0
        selBiggestStream = False

        for i in range(startofengstreams, startofengstreams + numOfEngSubs):  # Start iterating from the first sub

            #print("here3")
            #print(lineNum)

            if engSubStreams.find(str(lineNum) + "|") != -1:
                streamSize = compareSizes(lineNum, filename, currentOS)
                #print("here4")

                if numOfEngSubs == 2:  # Just select the biggest if theres only 2 subs
                    selBiggestStream = True
                    if streamSize > biggestStreamSize:
                        biggestStreamSize = streamSize
                        biggestStreamNum = lineNum
                elif numOfEngSubs > 2:  # select the second biggest if theres more then 2 subs
                    if streamSize > biggestStreamSize:
                        biggestStreamSize = streamSize
                    elif streamSize > secondBiggestStreamSize:
                        secondBiggestStreamSize = streamSize
                        secondBiggestStreamNum = lineNum

            lineNum += 1

        if selBiggestStream == True:
            metadataOptions += " -disposition:" + str(biggestStreamNum) + " default"
        else:
            metadataOptions += " -disposition:" + str(secondBiggestStreamNum) + " default"
        defaultSubSelected = True



    if signSongsSubStream != -1 and defaultSubSelected is False:  # Add an Sub Track if theres no eng/jpn one found
        mapThisStream = mapThisStream + str(signSongsSubStream) + " "
        metadataOptions += " -disposition:" + str(signSongsSubStream) + " default"

    # For removeSubsIfOnlyEngAudio
    if numOfEngAudio >= 1 and numOfJpnAudio == 0 and removeSubsIfOnlyEngAudio is True:  # If theres an Eng Audio and no JPN then:
        #print("removeSubsIfOnlyEngAudio Is On")
        metadataOptions = shadowMetadataOptions  # overwrite metadataOptions with only Eng Audios's
        mapThisStream = shadowMapThisStream  # overwrite metadataOptions with only Eng Audio's + video stream

    if numOfAudioStreams == 0:  # Add an Audio Track if theres no eng/jpn one found
        mapThisStream += firstAudioStreamMap + " "
        metadataOptions += " -disposition:" + str(firstAudioStreamNum) + " default"
        # print(str(firstAudioStreamNum)+"Hi")

    #txtfile = open("Metadata\\"+filename+"(stripped).txt") # map only v:a:s streams, not attachments

    numberOfMaps = ""
    lineNum = 0
    for line2 in range(0, totalNumOfStreams):

        # Populate temp variable with data from table
        metaCodecType = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_type"]).strip()

        # Don't add mjpeg, attachments, add everything else
        if metaCodecType != "mjpeg" or metaCodecType != "attachment":
            if mapThisStream.find(str(lineNum) + " ") != -1:
                numberOfMaps += " -map 0:"+str(lineNum)

        lineNum += 1

    #txtfile.close()
    #print(mapThisStream)

    metadataAndMaps = metadataOptions+numberOfMaps

    # Preview Output
    #print("")
    #print("+-------+------------Output Preview-+------------+----------+")
    #print(metadataTable2.get_string())
    #print("")

    return metadataAndMaps
