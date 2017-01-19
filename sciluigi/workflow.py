import logging
import luigi
import sciluigi

log = logging.getLogger('sciluigi-interface')


class WorkflowTask(sciluigi.task.Task):
    instance_name = luigi.Parameter(default='sciluigi_workflow')

    def configure_instance(self):
        self.initialize_tasks()
        self.initialize_inputs_and_outputs()
        self.connect_tasks()

    def initialize_tasks(self):
        raise NotImplementedError

    def connect_tasks(self):
        raise NotImplementedError

    def requires(self):
        log.info('Getting sub-workflow requirements for ' + self.__class__.__name__)
        #return self.endpoints

        return [output.sub_workflow_reqs for output in self.get_output_attrs()]
