#reference about apache beam dataframe: https://beam.apache.org/documentation/dsls/dataframes/overview/
#apache beam dataframe:
    # is a domain specific language (DSL) is an api to write pipeline with interface of pandas dataframe
    # it is build on top pandas dataframe
    # it add capacity of parallel processing of apache beam 
    # it also have vectorized of pandas
#note: have to to follow import syntax of the documenets otherwise we will have import and package error. which is import only function you need
#is it a good idea to use dataframe object in apache beam?
    #we have to convert between dataframe and pcollection object. which is not so good
    #for this specific test batch pipeline only
import apache_beam as beam
# from apache_beam.dataframe.io import read_csv
from apache_beam.io.filesystem import FileSystem as beam_fs
from apache_beam.io import fileio
from apache_beam.options.pipeline_options import PipelineOptions
import codecs
import csv
from typing import List, Dict, Iterable
import logging
import argparse

#define run function
#reference for using logging package (basic use): https://docs.python.org/3/howto/logging.html#basic-logging-tutorial
#reference for using argparse package: https://docs.python.org/3/howto/argparse.html

#command to run pipeline in your local:
    # python3 batch_pipeline.py --source_path="../data/test_data.csv" --dest_path="../data/dest"
########################################################## define apache beam pipeline component here

def expand_pattern(pattern: str) -> Iterable[str]:
    # print("pattern: ", pattern)
    for match_result in beam_fs.match([pattern])[0].metadata_list:
        yield match_result.path

def read_csv_lines(file_name: str) -> Iterable[Dict[str, str]]:
    with beam_fs.open(file_name) as f:
        # Beam reads files as bytes, but csv expects strings,
        # so we need to decode the bytes into utf-8 strings.
        for row in csv.DictReader(codecs.iterdecode(f, 'utf-8')):
            yield dict(row)
########################################################## combine apache beam component into complete pipeline here
def run(
    input_patterns: str,
    # dest_path: str,
    beam_args: List[str] = None
) -> None:
    #build your pipeline here
    #some change in the pipeline
    # input_pattern = [input_pattern]
    # print("input_pattern list: ", input_pattern)
    options = PipelineOptions(flags=[], type_check_additional='all')
    # print("input_patterns: ", input_patterns)
    with beam.Pipeline(options=options) as pipeline:
        readable_files = (
            pipeline
            | fileio.MatchFiles(input_patterns)
            | fileio.ReadMatches()
            | beam.Reshuffle()
        )
        files_and_contents = (
            readable_files
            | beam.Map(lambda x: x.read_utf8())
        )
        print_content = (
            files_and_contents
            | beam.Map(print)
        )
        write_to_file = (
            files_and_contents
            | beam.io.WriteToText(
            file_path_prefix="terraform_data_engineer/data/dest/",
            file_name_suffix=".csv"
            )
        )


############################################################ main program
#shell script will treat "terraform_data_engineer/"
#python3 terraform_data_engineer/beam_read_csv/pipeline_read_csv.py --input_pattern "terraform_data_engineer/data/*.csv"
if __name__ == "__main__":
    #do not need to init logging instance
    #some test change
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()

    #parse arguments
    parser.add_argument(
        "--input_patterns",
        help="an int number"
    )
    #return (namespace, list_of_args)
    args, beam_args = parser.parse_known_args()
    print("input_pattern: ", args.input_patterns)
    input_patterns = args.input_patterns
    run(
        input_patterns=input_patterns,
        # dest_path=args.dest_path,
        beam_args=beam_args
    )
