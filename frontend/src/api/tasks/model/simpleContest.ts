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
import { OlympiadLocation } from './olympiadLocation';
import { TargetClass } from './targetClass';
import { BaseContest } from './baseContest';


export interface SimpleContest { 
    academic_year?: number;
    readonly base_contest: BaseContest;
    composite_type: SimpleContest.CompositeTypeEnum;
    contest_duration?: number;
    readonly contest_id: number;
    deadline_for_appeal: string | null;
    end_date: string | null;
    end_of_enroll_date?: string | null;
    readonly enrolled?: boolean;
    holding_type: SimpleContest.HoldingTypeEnum;
    locations: Array<OlympiadLocation>;
    previous_contest_id?: number | null;
    previous_participation_condition: SimpleContest.PreviousParticipationConditionEnum;
    regulations?: string | null;
    result_publication_date?: string | null;
    readonly show_answer_after_contest?: boolean;
    show_result_after_finish?: boolean | null;
    start_date: string | null;
    status?: SimpleContest.StatusEnum;
    target_classes?: Array<TargetClass>;
    tasks_number?: number;
    total_points?: number;
    readonly user_count?: number;
    visibility: boolean;
}
export namespace SimpleContest {
    export type CompositeTypeEnum = 'SimpleContest';
    export const CompositeTypeEnum = {
        SimpleContest: 'SimpleContest' as CompositeTypeEnum
    };
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
    export type StatusEnum = 'Will start soon' | 'In progress' | 'Finished';
    export const StatusEnum = {
        WillStartSoon: 'Will start soon' as StatusEnum,
        InProgress: 'In progress' as StatusEnum,
        Finished: 'Finished' as StatusEnum
    };
}


