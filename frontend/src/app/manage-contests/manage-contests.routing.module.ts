import { RouterModule, Routes } from '@angular/router'
import { NgModule } from '@angular/core'
import { ManageBaseContestsComponent } from '@/manage-contests/containers/manage-base-contests/manage-base-contests.component'
import { ManageCompositeContestsComponent } from '@/manage-contests/containers/manage-composite-contests/manage-composite-contests.component'
import { ManageCompositeContestStagesComponent } from '@/manage-contests/containers/manage-composite-contest-stages/manage-composite-contest-stages.component'
import { ManageContestComponent } from '@/manage-contests/containers/manage-contest/manage-contest.component'
import { ManageContestVariantsComponent } from '@/manage-contests/containers/manage-contest-variants/manage-contest-variants.component'
import { ManageContestVariantTasksComponent } from '@/manage-contests/containers/manage-contest-variant-tasks/manage-contest-variant-tasks.component'
import { ManageContestUsersComponent } from '@/manage-contests/containers/manage-contest-users-component/manage-contest-users.component'
import { ManageContestUserAssignmentComponent } from '@/manage-contests/containers/manage-contest-user-assignment/manage-contest-user-assignment.component'
import { ManageContestsComponent } from '@/manage-contests/containers/manage-contests/manage-contests.component'
import { ManageTargetClassesComponent } from '@/manage-contests/components/manage-target-classes/manage-target-classes.component'
import { AdminAuthGuardService } from '@/shared/admin.auth.guard.service'


export const COMPONENTS = [
    ManageTargetClassesComponent,
    ManageBaseContestsComponent,
    ManageCompositeContestsComponent,
    ManageCompositeContestStagesComponent,
    ManageContestComponent,
    ManageContestUsersComponent,
    ManageContestUserAssignmentComponent,
    ManageContestVariantsComponent,
    ManageContestVariantTasksComponent,
    ManageContestsComponent
]

const routes: Routes =
    [
        {
            path: 'manage/contests/:baseContestId/contest/:simpleContestId/variants/:variantId/tasks',
            component: ManageContestVariantTasksComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/contest/:simpleContestId/variants',
            component: ManageContestVariantsComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/contest/:simpleContestId/users/:userId/assignment',
            component: ManageContestUserAssignmentComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/contest/:simpleContestId/users',
            component: ManageContestUsersComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId',
            component: ManageContestComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages',
            component: ManageCompositeContestStagesComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId',
            component: ManageCompositeContestsComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/allcontests',
            component: ManageContestsComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage/contests',
            component: ManageBaseContestsComponent,
            canActivate: [ AdminAuthGuardService ]
        },
        {
            path: 'manage', redirectTo: "manage/contests"
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ManageContestsRoutingModule {}