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
import { RangeTask } from './rangeTask';
import { MultipleChoiceTask } from './multipleChoiceTask';
import { PlainTask } from './plainTask';


/**
 * @type Task
 * @export
 */
export type Task = MultipleChoiceTask | PlainTask | RangeTask;

