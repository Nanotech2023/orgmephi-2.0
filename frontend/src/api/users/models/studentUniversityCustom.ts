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


export interface StudentUniversityCustom { 
    country: string;
    readonly known_type?: StudentUniversityCustom.KnownTypeEnum;
    university: string;
}
export namespace StudentUniversityCustom {
    export type KnownTypeEnum = 'Known' | 'Custom';
    export const KnownTypeEnum = {
        Known: 'Known' as KnownTypeEnum,
        Custom: 'Custom' as KnownTypeEnum
    };
}


