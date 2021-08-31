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
import { Location } from './location';


export interface SchoolInfo { 
    grade?: number | null;
    location?: Location;
    name?: string | null;
    number?: number | null;
    school_type?: SchoolInfo.SchoolTypeEnum | null;
    readonly user_id: number;
}
export namespace SchoolInfo {
    export type SchoolTypeEnum = 'School' | 'Lyceum' | 'Gymnasium' | 'EducationCenter' | 'NightSchool' | 'Technical' | 'External' | 'Collage' | 'ProfTech' | 'University' | 'Correctional' | 'Other';
    export const SchoolTypeEnum = {
        School: 'School' as SchoolTypeEnum,
        Lyceum: 'Lyceum' as SchoolTypeEnum,
        Gymnasium: 'Gymnasium' as SchoolTypeEnum,
        EducationCenter: 'EducationCenter' as SchoolTypeEnum,
        NightSchool: 'NightSchool' as SchoolTypeEnum,
        Technical: 'Technical' as SchoolTypeEnum,
        External: 'External' as SchoolTypeEnum,
        Collage: 'Collage' as SchoolTypeEnum,
        ProfTech: 'ProfTech' as SchoolTypeEnum,
        University: 'University' as SchoolTypeEnum,
        Correctional: 'Correctional' as SchoolTypeEnum,
        Other: 'Other' as SchoolTypeEnum
    };
}


