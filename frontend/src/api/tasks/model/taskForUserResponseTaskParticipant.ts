/**
 * aggregate_contest_tasks
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { AnswersInTaskRequestTaskParticipant } from './answersInTaskRequestTaskParticipant';


export interface TaskForUserResponseTaskParticipant { 
    answers?: Array<AnswersInTaskRequestTaskParticipant>;
    task_id: number;
    task_type?: TaskForUserResponseTaskParticipant.TaskTypeEnum;
}
export namespace TaskForUserResponseTaskParticipant {
    export type TaskTypeEnum = 'PlainTask' | 'RangeTask' | 'MultipleChoiceTask' | 'BaseTask';
    export const TaskTypeEnum = {
        PlainTask: 'PlainTask' as TaskTypeEnum,
        RangeTask: 'RangeTask' as TaskTypeEnum,
        MultipleChoiceTask: 'MultipleChoiceTask' as TaskTypeEnum,
        BaseTask: 'BaseTask' as TaskTypeEnum
    };
}


