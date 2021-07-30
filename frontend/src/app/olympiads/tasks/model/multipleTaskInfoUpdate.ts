/**
 * Tasks service API
 * API description in Markdown.
 *
 * OpenAPI spec version: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
import { MultipleTaskInfoAnswers } from './multipleTaskInfoAnswers';

/**
 * Request to update task with multiple choice
 */
export interface MultipleTaskInfoUpdate { 
    numOfTask?: number;
    imageOfTask?: Blob;
    answers?: Array<MultipleTaskInfoAnswers>;
}