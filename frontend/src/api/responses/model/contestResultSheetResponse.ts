/**
 * aggregate_contest_responses
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { UserResponseList } from './userResponseList';


export interface ContestResultSheetResponse { 
    contest_id: number;
    user_row: Array<UserResponseList>;
}

