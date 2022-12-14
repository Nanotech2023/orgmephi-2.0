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


export interface ContestResponseTaskCreator { 
    contest_duration?: number;
    contest_id: number;
    deadline_for_appeal?: string;
    end_date?: string;
    end_of_enroll_date?: string;
    holding_type?: ContestResponseTaskCreator.HoldingTypeEnum;
    location?: string;
    previous_contest_id?: number;
    previous_participation_condition?: ContestResponseTaskCreator.PreviousParticipationConditionEnum;
    result_publication_date?: string;
    show_result_after_finish?: boolean;
    start_date?: string;
    visibility: boolean;
}
export namespace ContestResponseTaskCreator {
    export type HoldingTypeEnum = 'OfflineContest' | 'OnLineContest';
    export const HoldingTypeEnum = {
        OfflineContest: 'OfflineContest' as HoldingTypeEnum,
        OnLineContest: 'OnLineContest' as HoldingTypeEnum
    };
    export type PreviousParticipationConditionEnum = 'Winner 1' | 'Winner 2' | 'Winner 3' | 'Diploma 1' | 'Diploma 2' | 'Diploma 3' | 'Participant';
    export const PreviousParticipationConditionEnum = {
        Winner1: 'Winner 1' as PreviousParticipationConditionEnum,
        Winner2: 'Winner 2' as PreviousParticipationConditionEnum,
        Winner3: 'Winner 3' as PreviousParticipationConditionEnum,
        Diploma1: 'Diploma 1' as PreviousParticipationConditionEnum,
        Diploma2: 'Diploma 2' as PreviousParticipationConditionEnum,
        Diploma3: 'Diploma 3' as PreviousParticipationConditionEnum,
        Participant: 'Participant' as PreviousParticipationConditionEnum
    };
}


