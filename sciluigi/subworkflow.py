import copy
import logging
import sciluigi

log = logging.getLogger('sciluigi-interface')


class SubWorkflowTask(sciluigi.task.Task):

    def __init__(self, *args, **kwargs):
        super(sciluigi.task.Task, self).__init__(*args, **kwargs)
        self.initialize_tasks()
        self.initialize_inputs_and_outputs()
        #self.endpoints = [self.connect_tasks()]
        self.connect_tasks()

    def initialize_tasks(self):
        raise NotImplementedError

    def new_task(self, instance_name, cls, **kwargs):
        instance_name = '%s_%s' % (self.instance_name, instance_name)
        if 'sciluigi_reduce_function' not in kwargs:
            wf_dict = copy.deepcopy(self.workflow_task.__dict__)
            # if '_tasks' in wf_dict:
            #     del wf_dict['_tasks']
            kwargs['sciluigi_reduce_args'] = (self, instance_name, cls, copy.deepcopy(kwargs), wf_dict)
            kwargs['sciluigi_reduce_function'] = sciluigi.task._new_task_unpickle
        return self.workflow_task.new_task(instance_name, cls, **kwargs)

    def connect_tasks(self):
        raise NotImplementedError

    def requires(self):
        log.info('Getting sub-workflow requirements for ' + self.__class__.__name__)
        #return self.endpoints

        return [output.sub_workflow_reqs for output in self.get_output_attrs()]
