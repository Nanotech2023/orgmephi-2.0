/**
 * aggregate_user
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { StudentUniversity } from './studentUniversity';


export interface StudentInfo { 
    grade?: number | null;
    phone?: string | null;
    university?: StudentUniversity | null;
    readonly user_id: number;
}

