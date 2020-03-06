import unittest
import copy
from gangagsoc.Initial_Task.countWord import * 

class TestInitialTask(unittest.TestCase):

    def test_exactword_count(self):
        cwd = os.path.abspath(os.getcwd())
        # 1st test for test.pdf
        job  = count_word_from_pdf(cwd+"/test/test.pdf",cwd+'/gangagsoc/Initial_Task/count_word.sh',cwd+'/gangagsoc/Initial_Task/merge_result.py')
        job.submit()
        check = check_job_until_completed(job)
        
        self.assertEqual(len(job.subjobs), 1)

        f_out = open("job_output.txt",'r')
        word_count = int(f_out.read())
        f_out.close()
        self.assertEqual(word_count, 2)

        # 2nd test for test2.pdf
        job  = count_word_from_pdf(cwd+"/test/test2.pdf",cwd+'/gangagsoc/Initial_Task/count_word.sh',cwd+'/gangagsoc/Initial_Task/merge_result.py')
        job.submit()
        check = check_job_until_completed(job)
        
        self.assertEqual(len(job.subjobs), 2)

        f_out = open("job_output.txt",'r')
        word_count = int(f_out.read())
        f_out.close()
        self.assertEqual(word_count, 5)

if __name__ == '__main__':
    unittest.main()
