import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    sns= boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:eu-west-2:684855629944:deployPortofolioTopic')
    
    try:
        s3 = boto3.resource('s3')
        portfolio_bucket = s3.Bucket('diwaan.org')
        build_bucket = s3.Bucket('diwan-build')
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('diwaan-build.zip', portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                print nm
                obj= myzip.open(nm) 
                portfolio_bucket.upload_fileobj(obj, nm,
                  ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]}) 
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print "Job Done"
        topic.publish(Subject="Portofolio deployed" , Message= "Portofolio deployed successfully")
    except:
        topic.publish(Subject="Portofolio Failed" , Message= "The Portofolio was not deployed successfully")
        raise
    
    return 'Hello from Lambda!'
    
