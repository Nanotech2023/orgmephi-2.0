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
import { SimpleContest } from './simpleContest';


export interface StageResponseTaskCreator { 
    condition?: StageResponseTaskCreator.ConditionEnum;
    contests?: Array<SimpleContest>;
    readonly stage_id?: number;
    stage_name: string;
    stage_num: number;
    this_stage_condition: string;
}
export namespace StageResponseTaskCreator {
    export type ConditionEnum = 'No' | 'And' | 'Or';
    export const ConditionEnum = {
        No: 'No' as ConditionEnum,
        And: 'And' as ConditionEnum,
        Or: 'Or' as ConditionEnum
    };
}


