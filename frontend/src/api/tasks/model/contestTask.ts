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
import { TaskPool } from './taskPool';


export interface ContestTask { 
    readonly contest_task_id?: number;
    num: number | null;
    task_points: number | null;
    readonly task_pools: Array<TaskPool>;
}

