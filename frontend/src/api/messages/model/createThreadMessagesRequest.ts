/**
 * aggregate_messages
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


export interface CreateThreadMessagesRequest { 
    category: string;
    message: string;
    related_contest?: number;
    thread_type: CreateThreadMessagesRequest.ThreadTypeEnum;
    topic: string;
}
export namespace CreateThreadMessagesRequest {
    export type ThreadTypeEnum = 'Appeal' | 'Work' | 'Contest' | 'General';
    export const ThreadTypeEnum = {
        Appeal: 'Appeal' as ThreadTypeEnum,
        Work: 'Work' as ThreadTypeEnum,
        Contest: 'Contest' as ThreadTypeEnum,
        General: 'General' as ThreadTypeEnum
    };
}


