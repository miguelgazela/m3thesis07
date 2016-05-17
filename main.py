from M3Parser import m3parser


def main():

    print "Starting..."

    parser = m3parser.M3Parser('email_dataset')
    parser.executeHousePartyProtocol()


if __name__ == "__main__":
    main()
