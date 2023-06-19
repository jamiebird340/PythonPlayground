import argparse
import plistlib
from itertools import count

import np as np
from matplotlib import pyplot


def findCommonTracks(fileNames):
    trackNameSets = []
    for fileName in fileNames:
        trackNames = set()
        plist = plistlib.readPlist(fileName)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except:
                pass
        trackNameSets.append(trackNames)
        commonTracks = set.intersection(*trackNameSets)

        if len(commonTracks) > 0:
            f = open("common.txt", "w")
            for val in commonTracks:
                s = "%s\n" % val
                f.write(s.encode("UTF-8"))
            f.close()
            print("%d common tracks found. "
                  "Track names written to common.txt." % len(commonTracks))
        else:
            print("No common tracks found")


def plotStats(fileName):
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']
    ratings = []
    durations = []

    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass

    if ratings == [] or durations == []:
        print("No valid data was collected")
        return

    x = np.array(durations, np.int32)
    x = x / 60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05 * np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    pyplot.show()


def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' % fileName)
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']
    trackNames = []

    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in trackNames:
                if duration // 1000 == trackNames[name][1]:
                    trackNames[name] = (duration, count + 1)
            else:
                trackNames[name] = (duration, 1)
        except:
            pass

        dups = []
        for k, v in trackNames.items():
            if v[1] > 1:
                dups.append((v[1], k))
        if len(dups) > 0:
            print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
        else:
            print("No duplicates found")

        f = open("dups.txt", 'w')
        for val in dups:
            f.write("[%d] %s\n" % (val[0], val[1]))
        f.close()


def main():
    descStr = "''"
    parser = argparse.ArgumentParser(description=descStr)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommonTracks(args.plFiles)
    elif args.plFile:
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for")


if __name__ == '__main__':
    main()
