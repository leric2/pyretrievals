"""
Some useful tools to populate and work with an Arts Workspace.
"""

from typhon.arts.workspace import Workspace


def new_workspace():
    return Workspace()


def include_general(ws):
    """
    Includes the general control files delivered with arts.

    :param ws: The Workspace
    """
    ws.execute_controlfile('general/general.arts')
    ws.execute_controlfile('general/agendas.arts')
    ws.execute_controlfile('general/continua.arts')
    ws.execute_controlfile('general/planet_earth.arts')


def copy_agendas(ws):
    """
    Copy default agendas used for most retrievals.

    :param ws: The Workspace
    """
    ws.Copy(ws.abs_xsec_agenda, ws.abs_xsec_agenda__noCIA)
    ws.Copy(ws.ppath_agenda, ws.ppath_agenda__FollowSensorLosPath)
    ws.Copy(ws.ppath_step_agenda, ws.ppath_step_agenda__GeometricPath)
    ws.Copy(ws.iy_space_agenda, ws.iy_space_agenda__CosmicBackground)
    ws.Copy(ws.iy_surface_agenda, ws.iy_surface_agenda__UseSurfaceRtprop)
    ws.Copy(ws.iy_main_agenda, ws.iy_main_agenda__Emission)
    ws.Copy(ws.propmat_clearsky_agenda, ws.propmat_clearsky_agenda__OnTheFly)


def set_basics(ws, atmosphere_dim=1, iy_unit='RJBT', ppath_lmax=-1, stokes_dim=1):
    """
    Set important workspace variables do sensible defaults.

    :param ws: The workspace.
    :param atmosphere_dim:
    :param iy_unit:
    :param ppath_lmax:
    :param stokes_dim:
    """
    # We run the checks here, because Arts gives the errors only later
    if atmosphere_dim not in [1, 2, 3]:
        raise ValueError('atmosphere_dim must be 1, 2 or 3.')
    if stokes_dim not in [1, 2, 3, 4]:
        raise ValueError('stokes_dim must be 1, 2, 3 or 4.')
    valid_iy_units = ['1', 'RJBT', 'PlanckBT', 'W/(m^2 m sr)', 'W/(m^2 m-1 sr)']
    if iy_unit not in valid_iy_units:
        raise ValueError('iy_unit must be one of ' + ', '.join(valid_iy_units))

    if atmosphere_dim == 1:
        ws.AtmosphereSet1D()
    elif atmosphere_dim == 2:
        ws.AtmosphereSet2D()
    elif atmosphere_dim == 3:
        ws.AtmosphereSet3D()

    ws.stokes_dim = stokes_dim
    ws.iy_unit = iy_unit
    ws.ppath_lmax = float(ppath_lmax)


def setup_spectroscopy(ws, abs_lines, abs_species, line_shape=None):
    """
    Setup absorption species and spectroscopy data.

    :param ws: The workspace.
    :param abs_lines: Absoption lines.
    :param abs_species: List of abs species tags.
    :param line_shape: Line shape definition. Default: ['Voigt_Kuntz6', 'VVH', 750e9]
    :type abs_lines: typhon.arts.catalogues.ArrayOfLineRecord
    """
    if line_shape is None:
        line_shape = ['Voigt_Kuntz6', 'VVH', 750e9]
    ws.abs_speciesSet(abs_species)
    ws.abs_lineshapeDefine(*line_shape)
    ws.abs_lines = abs_lines
    ws.abs_lines_per_speciesCreateFromLines()


def run_checks(ws, negative_vmr_ok=False):
    """
    Run common checkedCalc methods.
    :param ws: The Workspace
    """
    negative_vmr_ok = 1 if negative_vmr_ok else 0

    ws.abs_xsec_agenda_checkedCalc()
    ws.propmat_clearsky_agenda_checkedCalc()
    ws.atmfields_checkedCalc(negative_vmr_ok=negative_vmr_ok)
    ws.atmgeom_checkedCalc()
    ws.cloudbox_checkedCalc()
    ws.sensor_checkedCalc()


if __name__ == '__main__':
    ws = Workspace()
    include_general(ws)
    copy_agendas(ws)
    set_basics(ws, atmosphere_dim=3)
    run_checks(ws)
