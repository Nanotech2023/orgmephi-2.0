import { Component, OnInit, ViewChild } from '@angular/core'
import { UserFull } from '@api/users/models'
import { ManageUsersStore } from '@/manage-users/manage-users.store'
import { Observable } from 'rxjs'
import { DxDataGridComponent } from 'devextreme-angular'
import { ActivatedRoute, Router } from '@angular/router'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ],
    providers: [ ManageUsersStore ]
} )
export class ManageUsersComponent implements OnInit
{
    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    users$: Observable<UserFull[]> = this.store.users$
    selectedRowIndex: number = -1
    selectedRow?: UserFull = undefined
    userTypeEnum: ( "PreUniversity" | "Enrollee" | "School" | "University" | "Internal" | "PreRegister" )[] = Object.values( UserFull.TypeEnum )
    userRoleEnum: ( "Unconfirmed" | "Participant" | "Creator" | "Admin" | "System" )[] = Object.values( UserFull.RoleEnum )

    constructor( private route: ActivatedRoute, private router: Router, private store: ManageUsersStore ) {}

    ngOnInit(): void
    {
        this.store.reload()
    }

    editRow(): void
    {
        this.grid.instance.editRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    deleteRow(): void
    {
        this.grid.instance.deleteRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    addRow(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
    }

    selectedChanged( e: any ): void
    {
        this.selectedRowIndex = e.component.getRowIndexByKey( e.selectedRowKeys[ 0 ] )
    }

    navigateElement(): void
    {
        if ( this.selectedRow )
            this.router.navigate( [ this.selectedRow.id, 'contests' ], { relativeTo: this.route } )
    }
}
