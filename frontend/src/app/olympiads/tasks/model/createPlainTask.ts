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

/**
 * Request to creation task with plain text
 */
export interface CreatePlainTask { 
    numOfTask: number;
    imageOfTask: Blob;
    recommendedAnswer: string;
}