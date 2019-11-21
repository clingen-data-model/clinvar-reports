import argparse
from ExcelReportsFunctions import *


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--downloadonly",
                        help="Download the files from clinvar FTP, but dont process them",
                        action="store_true",
                        dest="download_only")
    parser.add_argument("-e", "--existingfiles",
                        help="Don’t download FTP files from clinvar, use existing files",
                        action="store_true",
                        dest="use_exisiting_files")
    parser.add_argument("-r", "--retainfiles",
                        help="Don’t remove the clinvar FTP files after processing",
                        action="store_true",
                        dest="retain_files")
    parser.add_argument("-u", "--usedate",
                        help="Use date for when creating directories in the form MM-DD-YYYY",
                        dest="use_date")
    parser.add_argument("stars", choices=["ZeroStar", "OneStar"])
    args = parser.parse_args()

    variation_archive = 'ClinVarVariationRelease_00-latest.xml.gz'
    variation_allele = 'variation_allele.txt.gz'
    variation_summary = 'variant_summary.txt.gz'
    submission_summary = 'submission_summary.txt.gz'
    ftp_var_archive_dir = '/pub/clinvar/xml/clinvar_variation/'
    ftp_tab_delimited_dir = '/pub/clinvar/tab_delimited/'

    dir = 'ClinVar' + args.stars + 'Reports'

    if not args.use_exisiting_files:
        get_file(variation_archive, ftp_var_archive_dir)
        get_file(variation_allele, ftp_tab_delimited_dir)
        get_file(variation_summary, ftp_tab_delimited_dir)
        get_file(submission_summary, ftp_tab_delimited_dir)

    if not args.use_date:
        date = get_file_date(submission_summary, ftp_tab_delimited_dir)
    else:
        date = args.use_date

    if args.download_only:
        sys.exit(0)

    create_orgDict(variation_archive, args.retain_files)
    create_a2vHash(variation_allele, args.retain_files)
    create_HGVSHash(variation_summary, args.retain_files)
    create_scvHash(submission_summary, args.stars, args.retain_files)

    ExcelDir = make_directory(dir, date, args.stars)

    excelFile = args.stars + 'Report_' + date + '.xlsx'
    distFile = '_' + args.stars + 'DistributionReport_' + date + '.xlsx'

    statFile = '_' + args.stars + 'ReportsStats_' + date + '.xlsx'

    create_files(ExcelDir, excelFile, date, statFile, args.stars)
    create_distFile(ExcelDir, distFile, date, args.stars)

main()
