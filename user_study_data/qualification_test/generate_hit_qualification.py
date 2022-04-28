import boto3

aws_access_key_id = 'AKIAWGKDJGMAZJGGAFKY'
aws_secret_access_key = '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'


questions = open('color_qs.xml', mode='r').read()
answers = open('color_ans_key.xml', mode='r').read()

mturk = boto3.client('mturk',
                      aws_access_key_id = aws_access_key_id,
                      aws_secret_access_key = aws_secret_access_key, 
                      region_name='us-east-1', 
                      endpoint_url='https://mturk-requester.us-east-1.amazonaws.com')

qual_response = mturk.create_qualification_type(
                        Name='TrustedImageWorker',
                        Keywords='image completion, realistic image',
                        Description='Simple and naive test to identify good worker.',
                        QualificationTypeStatus='Active',
                        Test=questions,
                        AnswerKey=answers,
                        TestDurationInSeconds=300)

print(qual_response['QualificationType']['QualificationTypeId'])

