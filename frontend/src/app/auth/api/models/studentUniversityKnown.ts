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


export interface StudentUniversityKnown { 
    readonly country?: string;
    readonly known_type?: StudentUniversityKnown.KnownTypeEnum;
    university: string;
}
export namespace StudentUniversityKnown {
    export type KnownTypeEnum = 'Known';
    export const KnownTypeEnum = {
        Known: 'Known' as KnownTypeEnum
    };
}


