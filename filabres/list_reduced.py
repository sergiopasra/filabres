import fnmatch
import json
import pandas as pd


def list_reduced(img1, img2, instrument, args_night):
    """
    Display list with already classified images of the selected type

    Parameters
    ==========
    img1 : str or None
        Image type. It should coincide with any of the available
        image types declared in the instrument configuration file.
        Each file name is displayed in a different line, together
        with the quantile information.
    img2 : str or None
        Image type. It should coincide with any of the available
        image types declared in the instrument configuration file.
        The file names are listed in a single line, separated by a
        single blank space.
    instrument : str
        Instrument name.
    args_night : str or None
        Selected night
    """

    if img2 is None:
        if img1 is None:
            return
        else:
            imagetype = img1
    else:
        if img1 is None:
            imagetype = img2
        else:
            print('ERROR: do not use -lr and -lrf simultaneously.')
            raise SystemExit()

    # read database
    databasefile = 'filabres_db_{}_{}.json'.format(instrument, imagetype)

    try:
        with open(databasefile) as jfile:
            database = json.load(jfile)
    except FileNotFoundError:
        msg = 'File {} not found'.format(databasefile)
        raise SystemError(msg)

    df = None  # Avoid PyCharm warning

    # check for imagetype
    if imagetype not in database:
        raise SystemExit()

    if args_night is None:
        night = '*'
    else:
        night = args_night

    n = 0
    colnames = None
    sortedkeys = database['sortedkeys']

    for ssig in database[imagetype]:
        if ssig == "sortedkeys":
            pass
        else:
            for mjdobs in database[imagetype][ssig]:
                outfile = database[imagetype][ssig][mjdobs]['filename']
                nightok = fnmatch.fnmatch(
                    database[imagetype][ssig][mjdobs]['night'],
                    night
                )
                if nightok:
                    n += 1
                    if img2 is not None:
                        print(outfile, end=' ')
                    else:
                        statsumm = \
                            database[imagetype][ssig][mjdobs]['statsumm']
                        colnames_ = ['file'] + sortedkeys + ['NORIGIN']
                        colnames_ += list(statsumm.keys())
                        if n == 1:
                            colnames = colnames_
                            df = pd.DataFrame(columns=colnames)
                        else:
                            if colnames_ != colnames:
                                print("ERROR: number of keywords do not match"
                                      "for file {}".format(outfile))
                                print("- expected:", colnames)
                                print("- required:", colnames_)
                                raise SystemExit()

                        # new_df_row = [os.path.basename(outfile)]
                        norigin = database[imagetype][ssig][mjdobs]['norigin']
                        signature = \
                            database[imagetype][ssig][mjdobs]['signature']
                        new_df_row = [outfile]
                        for keyword in sortedkeys:
                            new_df_row += [signature[keyword]]
                        new_df_row += [norigin]
                        new_df_row += list(statsumm.values())
                        df.loc[n-1] = new_df_row

    if img2 is not None:
        if n > 0:
            print()
    else:
        if df is not None:
            if df.shape[0] > 0:
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', -1)
                print(df.round(1).to_string(index=True))

    raise SystemExit()
